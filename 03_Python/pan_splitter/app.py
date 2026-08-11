"""
Panorama Pro — Instagram carousel slicer for Pythonista 3.

Loads a photo, allows free-angle rotation via two-finger gesture,
then crops the image into exactly two 4:5 (1080x1350) frames for
seamless Instagram panoramic carousels. Preserves original file
format (HEIC, JPEG, PNG) and filename on export.

Two-phase workflow
------------------
1. **Edit mode** — rotate the image with two fingers or the +90 button.
2. **Crop mode** — drag and pinch-to-resize a 2-slice 4:5 frame,
   then slice and save to the Camera Roll.
"""

import ui
import photos
from PIL import Image
import io
import os
import tempfile
import console
import math

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HAS_HEIF = True
except ImportError:
    HAS_HEIF = False


class EditCanvas(ui.View):
    """Touch-enabled canvas for image rotation in Edit mode.

    Tracks two-finger gestures to compute a cumulative rotation angle
    and delegates the PIL re-render to the parent ``PanoramaPro`` app
    once fingers are lifted.

    Parameters
    ----------
    app : PanoramaPro
        Parent application view that owns the rotation state.

    Attributes
    ----------
    ROTATE_THRESHOLD : float
        Minimum angle delta (degrees) required to trigger a re-render
        on touch end, avoiding unnecessary PIL work for tiny jitters.
    active_touches : dict
        Maps ``touch_id`` to the latest ``(x, y)`` location.
    gesture : str or None
        Current gesture type; ``'rotate'`` or ``None``.
    prev_angle : float or None
        Previous two-finger angle in radians, used for delta calculation.
    """

    ROTATE_THRESHOLD = 2

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.multitouch_enabled = True
        self.background_color = '#111'

        self.image_view = ui.ImageView()
        self.image_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        self.add_subview(self.image_view)

        self.active_touches = {}
        self.gesture = None
        self.prev_angle = None
        self._gesture_started_angle = 0.0

    def layout(self):
        """Fill the canvas bounds with the image view."""
        self.image_view.frame = self.bounds

    def set_image(self, ui_img):
        """Replace the displayed ``ui.Image``.

        Parameters
        ----------
        ui_img : ui.Image
            Image to display in the canvas.
        """
        self.image_view.image = ui_img

    def touch_began(self, touch):
        """Register a new finger and start rotation when two are down."""
        if self.app.mode != 'edit':
            return
        self.active_touches[touch.touch_id] = touch.location
        if len(self.active_touches) >= 2:
            self.gesture = 'rotate'
            pts = list(self.active_touches.values())[:2]
            self.prev_angle = math.atan2(
                pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])
            self._gesture_started_angle = self.app.rotation_angle

    def touch_moved(self, touch):
        """Accumulate rotation delta while two fingers move."""
        if self.app.mode != 'edit':
            return
        self.active_touches[touch.touch_id] = touch.location

        if self.gesture == 'rotate' and len(self.active_touches) >= 2:
            pts = list(self.active_touches.values())[:2]
            ca = math.atan2(
                pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])
            if self.prev_angle is not None:
                da = math.degrees(ca - self.prev_angle)
                if da > 180:
                    da -= 360
                elif da < -180:
                    da += 360
                self.app.rotation_angle += da
            self.prev_angle = ca
            self.app._update_edit_label()

    def touch_ended(self, touch):
        """Trigger a PIL re-render if rotation exceeded the threshold."""
        self.active_touches.pop(touch.touch_id, None)
        if not self.active_touches:
            if self.gesture == 'rotate':
                delta = abs(
                    self.app.rotation_angle - self._gesture_started_angle)
                if delta > self.ROTATE_THRESHOLD:
                    self.app._render_edit_preview()
            self.gesture = None
            self.prev_angle = None
        elif len(self.active_touches) == 1:
            self.gesture = None
            self.prev_angle = None


class CropOverlay(ui.View):
    """Interactive 2-slice crop frame overlay for Crop mode.

    Displays a movable, resizable rectangle that always maintains a
    2 x 4:5 aspect ratio (total 8:5). The area outside the frame is
    darkened with semi-transparent mask views. A vertical midline and
    numbered labels indicate the two slices.

    Gestures
    --------
    - **One finger** : drag to reposition the crop frame.
    - **Two fingers** : pinch to resize (scale 0.2–1.0 of image height).

    Attributes
    ----------
    DARK : tuple
        RGBA colour for the semi-transparent mask regions.
    crop_scale : float
        Fraction of image display height used by the crop frame (0.2–1.0).
    off_x : float
        Normalised horizontal offset of the crop frame (0.0–1.0).
    off_y : float
        Normalised vertical offset of the crop frame (0.0–1.0).
    """

    DARK = (0, 0, 0, 0.55)

    def __init__(self):
        super().__init__()
        self.multitouch_enabled = True
        self.touch_enabled = True
        self.background_color = None

        self.crop_scale = 1.0
        self.off_x = 0.5
        self.off_y = 0.5
        self._img_rect = (0, 0, 100, 100)

        self._masks = []
        for _ in range(4):
            m = ui.View()
            m.background_color = self.DARK
            m.touch_enabled = False
            self._masks.append(m)
            self.add_subview(m)

        self._mid_line = ui.View()
        self._mid_line.background_color = (1, 1, 1, 0.85)
        self._mid_line.touch_enabled = False
        self.add_subview(self._mid_line)

        self._border = ui.View()
        self._border.background_color = None
        self._border.border_color = (1, 1, 1, 0.85)
        self._border.border_width = 2
        self._border.touch_enabled = False
        self.add_subview(self._border)

        self._lbl1 = self._make_lbl('1')
        self._lbl2 = self._make_lbl('2')

        self.active_touches = {}
        self._gesture = None
        self._drag_origin = None
        self._drag_base = None
        self._pinch_base_dist = None
        self._pinch_base_scale = None

    def _make_lbl(self, txt):
        """Create a small numbered pill label and add it as a subview.

        Parameters
        ----------
        txt : str
            Label text (e.g. ``'1'``, ``'2'``).

        Returns
        -------
        ui.Label
            The configured label subview.
        """
        lb = ui.Label()
        lb.text = txt
        lb.text_color = 'white'
        lb.font = ('<system-bold>', 14)
        lb.alignment = ui.ALIGN_CENTER
        lb.background_color = (0, 0, 0, 0.4)
        lb.corner_radius = 4
        lb.touch_enabled = False
        self.add_subview(lb)
        return lb

    def configure(self, cw, ch, img_w, img_h):
        """Recompute the image display rect and reset crop position.

        Parameters
        ----------
        cw : float
            Canvas width in points.
        ch : float
            Canvas height in points.
        img_w : int
            Source image width in pixels.
        img_h : int
            Source image height in pixels.
        """
        if img_h == 0 or img_w == 0:
            return
        ratio = img_w / img_h
        vratio = cw / ch
        if ratio > vratio:
            dw, dh = cw, cw / ratio
        else:
            dh, dw = ch, ch * ratio
        self._img_rect = ((cw - dw) / 2, (ch - dh) / 2, dw, dh)
        self.crop_scale = 1.0
        self.off_x = 0.5
        self.off_y = 0.5
        self._layout_crop()

    def _crop_rect(self):
        """Compute the crop frame rectangle in overlay coordinates.

        The frame maintains a 2 x 4:5 aspect ratio (width = height * 1.6).
        If the computed width exceeds the image display width, the height
        is reduced proportionally.

        Returns
        -------
        tuple of float
            ``(fx, fy, fw, fh)`` — origin and size of the crop frame.
        """
        dx, dy, dw, dh = self._img_rect
        fh = dh * self.crop_scale
        fw = fh * 1.6
        if fw > dw:
            fw = dw
            fh = fw / 1.6
        spare_x = max(0.0, dw - fw)
        spare_y = max(0.0, dh - fh)
        fx = dx + self.off_x * spare_x
        fy = dy + self.off_y * spare_y
        return fx, fy, fw, fh

    def _layout_crop(self):
        """Position mask views, border, midline, and labels."""
        w, h = self.width, self.height
        if w < 1 or h < 1:
            return
        fx, fy, fw, fh = self._crop_rect()

        top, bot, left, right = self._masks
        top.frame = (0, 0, w, max(0, fy))
        bot.frame = (0, fy + fh, w, max(0, h - fy - fh))
        left.frame = (0, fy, max(0, fx), fh)
        right.frame = (fx + fw, fy, max(0, w - fx - fw), fh)

        self._border.frame = (fx, fy, fw, fh)

        mid_x = fx + fw / 2
        self._mid_line.frame = (mid_x - 0.5, fy, 1.0, fh)

        sw = fw / 2
        self._lbl1.frame = (fx + sw / 2 - 14, fy + fh - 32, 28, 22)
        self._lbl2.frame = (fx + sw + sw / 2 - 14, fy + fh - 32, 28, 22)

    def crop_pixels(self, img_w, img_h):
        """Map the display-space crop frame to source image pixel coords.

        Parameters
        ----------
        img_w : int
            Source image width in pixels.
        img_h : int
            Source image height in pixels.

        Returns
        -------
        tuple of int or None
            ``(cx, cy, cw, ch)`` in pixels, or ``None`` if the display
            rect is too small.
        """
        dx, dy, dw, dh = self._img_rect
        if dw < 1 or dh < 1:
            return None
        px_per_pt = img_w / dw
        fx, fy, fw, fh = self._crop_rect()
        cx = (fx - dx) * px_per_pt
        cy = (fy - dy) * px_per_pt
        cw = fw * px_per_pt
        ch = fh * px_per_pt
        return int(cx), int(cy), int(cw), int(ch)

    # -- Touch handling ----------------------------------------------------

    def touch_began(self, touch):
        """Start drag or pinch gesture depending on finger count."""
        self.active_touches[touch.touch_id] = touch.location
        n = len(self.active_touches)
        if n >= 2:
            self._gesture = 'pinch'
            pts = list(self.active_touches.values())[:2]
            self._pinch_base_dist = math.hypot(
                pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
            self._pinch_base_scale = self.crop_scale
        elif n == 1:
            self._gesture = 'drag'
            self._drag_origin = touch.location
            self._drag_base = (self.off_x, self.off_y)

    def touch_moved(self, touch):
        """Update crop frame position (drag) or scale (pinch)."""
        self.active_touches[touch.touch_id] = touch.location

        if self._gesture == 'pinch' and len(self.active_touches) >= 2:
            pts = list(self.active_touches.values())[:2]
            d = math.hypot(
                pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
            if self._pinch_base_dist and self._pinch_base_dist > 10:
                ratio = d / self._pinch_base_dist
                self.crop_scale = max(
                    0.2, min(1.0, self._pinch_base_scale * ratio))
                self._layout_crop()

        elif self._gesture == 'drag' and len(self.active_touches) == 1:
            dx, dy, dw, dh = self._img_rect
            fx, fy, fw, fh = self._crop_rect()
            spare_x = max(1.0, dw - fw)
            spare_y = max(1.0, dh - fh)
            loc = touch.location
            px = loc[0] - self._drag_origin[0]
            py = loc[1] - self._drag_origin[1]
            self.off_x = max(
                0.0, min(1.0, self._drag_base[0] + px / spare_x))
            self.off_y = max(
                0.0, min(1.0, self._drag_base[1] + py / spare_y))
            self._layout_crop()

    def touch_ended(self, touch):
        """Transition from pinch back to drag when one finger remains."""
        self.active_touches.pop(touch.touch_id, None)
        if not self.active_touches:
            self._gesture = None
        elif len(self.active_touches) == 1:
            self._gesture = 'drag'
            pt = list(self.active_touches.values())[0]
            self._drag_origin = pt
            self._drag_base = (self.off_x, self.off_y)


class ScrollDelegate:
    """Updates the page indicator label as the carousel scrolls.

    Parameters
    ----------
    app : PanoramaPro
        Parent application view that owns the page label.
    """

    def __init__(self, app):
        self.app = app

    def scrollview_did_scroll(self, sv):
        """Callback fired by the ``ui.ScrollView`` on content offset change.

        Parameters
        ----------
        sv : ui.ScrollView
            The scroll view that fired the event.
        """
        if sv.width > 0 and self.app.slices:
            page = int(sv.content_offset[0] / sv.width + 0.5)
            total = len(self.app.slices)
            self.app.page_label.text = f'{min(page + 1, total)} / {total}'


class PanoramaPro(ui.View):
    """Main application view — two-phase Instagram panoramic slicer.

    Phase 1 (Edit mode):
        Load a photo, rotate it freely with two fingers or the +90
        button, then tap **Crop >>** to lock the orientation.

    Phase 2 (Crop mode):
        A 2-slice 4:5 crop frame appears over the baked image. Drag
        with one finger to reposition, pinch with two fingers to
        resize. Tap **Slice** to generate the two 1080x1350 frames,
        preview them in the carousel, and **Save** to Camera Roll.

    Attributes
    ----------
    THUMB_MAX_W : int
        Maximum thumbnail width used for on-screen previews to keep
        PIL operations fast.
    mode : str
        Current phase — ``'edit'`` or ``'crop'``.
    raw_img : PIL.Image.Image or None
        Original full-resolution image as loaded.
    thumb_img : PIL.Image.Image or None
        Down-scaled preview thumbnail.
    baked_img : PIL.Image.Image or None
        Full-resolution image with rotation baked in (created on
        entering crop mode).
    slices : list of PIL.Image.Image
        The two 1080x1350 output frames after slicing.
    rotation_angle : float
        Cumulative rotation in degrees.
    """

    THUMB_MAX_W = 1200

    def __init__(self):
        super().__init__()
        self.background_color = '#1a1a1a'
        self.name = 'Panorama Pro'

        self.mode = 'edit'
        self.raw_img = None
        self.thumb_img = None
        self.baked_img = None
        self.slices = []
        self._img_fmt = 'PNG'
        self._img_name = 'photo'

        self.rotation_angle = 0.0

        self.load_btn = self._btn('Load', '#007AFF', self.pick_image)
        self.rot90_btn = self._btn('+90\u00b0', '#5856D6', self.rotate_90)
        self.reset_btn = self._btn('Reset', '#FF3B30', self.reset_angle)
        self.crop_btn = self._btn('Crop >>', '#FF9500', self.enter_crop)
        self._edit_btns = [
            self.load_btn, self.rot90_btn,
            self.reset_btn, self.crop_btn,
        ]

        self.back_btn = self._btn('<< Back', '#8E8E93', self.enter_edit)
        self.slice_btn = self._btn('Slice', '#FF9500', self.do_slice)
        self.save_btn = self._btn('Save', '#34C759', self.save_slices)
        self.save_btn.alpha = 0
        self._crop_btns = [self.back_btn, self.slice_btn, self.save_btn]

        for b in self._edit_btns + self._crop_btns:
            self.add_subview(b)

        self.canvas = EditCanvas(self)
        self.add_subview(self.canvas)

        self.crop_overlay = CropOverlay()

        self.info_label = self._label('Load an image to begin')
        self.add_subview(self.info_label)

        self.scroll = ui.ScrollView()
        self.scroll.paging_enabled = True
        self.scroll.shows_horizontal_scroll_indicator = False
        self.scroll.background_color = '#000'
        self.scroll.delegate = ScrollDelegate(self)
        self.add_subview(self.scroll)

        self.page_label = ui.Label()
        self.page_label.text_color = 'white'
        self.page_label.font = ('<system-bold>', 14)
        self.page_label.alignment = ui.ALIGN_CENTER
        self.page_label.background_color = (0, 0, 0, 0.5)
        self.page_label.corner_radius = 10
        self.page_label.text = ''
        self.add_subview(self.page_label)

        self._sync_toolbar()

    # -- Factory helpers ---------------------------------------------------

    @staticmethod
    def _btn(title, bg, action):
        """Create a rounded toolbar button.

        Parameters
        ----------
        title : str
            Button label text.
        bg : str
            Hex background colour.
        action : callable
            Callback fired on tap.

        Returns
        -------
        ui.Button
        """
        b = ui.Button(title=title)
        b.background_color = bg
        b.tint_color = 'white'
        b.corner_radius = 8
        b.action = action
        return b

    @staticmethod
    def _label(text):
        """Create a centred info label.

        Parameters
        ----------
        text : str
            Initial label text.

        Returns
        -------
        ui.Label
        """
        lb = ui.Label()
        lb.text = text
        lb.text_color = '#aaa'
        lb.font = ('<system>', 13)
        lb.alignment = ui.ALIGN_CENTER
        return lb

    def _sync_toolbar(self):
        """Show or hide toolbar buttons based on current mode."""
        is_edit = self.mode == 'edit'
        for b in self._edit_btns:
            b.hidden = not is_edit
        for b in self._crop_btns:
            b.hidden = is_edit

    # -- Layout ------------------------------------------------------------

    def layout(self):
        """Reposition all subviews for the current screen size and mode."""
        w, h = self.width, self.height
        bar_y = 60
        btn_h = 38
        pad = 8

        btns = self._edit_btns if self.mode == 'edit' else self._crop_btns
        btn_w = (w - pad * (len(btns) + 1)) / len(btns) if btns else 0
        for i, b in enumerate(btns):
            b.frame = (pad + i * (btn_w + pad), bar_y, btn_w, btn_h)
        hidden = self._crop_btns if self.mode == 'edit' else self._edit_btns
        for b in hidden:
            b.frame = (-999, 0, 0, 0)

        lbl_h = 22
        canvas_top = bar_y + btn_h + pad
        canvas_h = (h - canvas_top) * 0.55
        self.canvas.frame = (0, canvas_top, w, canvas_h)

        if self.crop_overlay.superview:
            self.crop_overlay.frame = (0, canvas_top, w, canvas_h)
            if self.baked_img:
                self.crop_overlay.configure(
                    w, canvas_h, *self.baked_img.size)

        self.info_label.frame = (0, canvas_top + canvas_h + 2, w, lbl_h)

        car_top = canvas_top + canvas_h + lbl_h + pad
        car_h = h - car_top
        self.scroll.frame = (0, car_top, w, car_h)

        for i, sv in enumerate(self.scroll.subviews):
            sv.frame = (i * w, 0, w, car_h)
        if self.slices:
            self.scroll.content_size = (w * len(self.slices), 0)

        pl_w, pl_h = 70, 28
        self.page_label.frame = (
            (w - pl_w) / 2, car_top + car_h - pl_h - 8, pl_w, pl_h)

    # -- Image helpers -----------------------------------------------------

    def _thumb(self, img):
        """Down-scale an image for preview if wider than ``THUMB_MAX_W``.

        Parameters
        ----------
        img : PIL.Image.Image
            Source image.

        Returns
        -------
        PIL.Image.Image
            Thumbnail (or copy if already small enough).
        """
        w, h = img.size
        if w <= self.THUMB_MAX_W:
            return img.copy()
        r = self.THUMB_MAX_W / w
        return img.resize((self.THUMB_MAX_W, int(h * r)), Image.LANCZOS)

    def _to_ui(self, pil, quality=85):
        """Convert a PIL image to a ``ui.Image`` via JPEG encoding.

        Parameters
        ----------
        pil : PIL.Image.Image
            Image to convert.
        quality : int, optional
            JPEG quality (default 85).

        Returns
        -------
        ui.Image
        """
        with io.BytesIO() as buf:
            pil.save(buf, format='JPEG', quality=quality)
            return ui.Image.from_data(buf.getvalue())

    def _rotate_thumb(self):
        """Apply the current rotation angle to the thumbnail.

        Returns
        -------
        PIL.Image.Image or None
            Rotated thumbnail, or ``None`` if no thumbnail is loaded.
        """
        if not self.thumb_img:
            return self.thumb_img
        angle = self.rotation_angle % 360
        if angle == 0:
            return self.thumb_img
        return self.thumb_img.rotate(
            -angle, expand=True,
            resample=Image.BICUBIC, fillcolor=(0, 0, 0))

    def _render_edit_preview(self):
        """Re-render the rotated thumbnail and update the canvas."""
        if not self.thumb_img:
            return
        rotated = self._rotate_thumb()
        self.canvas.set_image(self._to_ui(rotated))

    def _update_edit_label(self):
        """Update the info label with the current rotation angle."""
        a = self.rotation_angle % 360
        if a > 180:
            a -= 360
        self.info_label.text = f'Angle: {a:.1f}\u00b0'

    def _update_crop_label(self):
        """Update the info label with crop mode instructions."""
        if not self.baked_img:
            return
        self.info_label.text = '2 slices  \u00b7  drag to move \u00b7 pinch to resize'

    # -- Mode switching ----------------------------------------------------

    def enter_crop(self, sender):
        """Bake the rotation into the full-res image and enter Crop mode.

        Parameters
        ----------
        sender : ui.Button
            The button that triggered the action.
        """
        if not self.raw_img:
            console.hud_alert('Load an image first')
            return

        angle = self.rotation_angle % 360
        if angle == 0:
            self.baked_img = self.raw_img.copy()
        else:
            self.baked_img = self.raw_img.rotate(
                -angle, expand=True,
                resample=Image.BICUBIC, fillcolor=(0, 0, 0))

        self.mode = 'crop'
        self._sync_toolbar()

        thumb = self._thumb(self.baked_img)
        self.canvas.set_image(self._to_ui(thumb))

        self.add_subview(self.crop_overlay)
        self.crop_overlay.frame = self.canvas.frame
        self.crop_overlay.configure(
            self.canvas.width, self.canvas.height,
            *self.baked_img.size)

        self._update_crop_label()
        self.layout()
        console.hud_alert('Drag the crop frame')

    def enter_edit(self, sender):
        """Remove the crop overlay and return to Edit mode.

        Parameters
        ----------
        sender : ui.Button
            The button that triggered the action.
        """
        self.mode = 'edit'
        self._sync_toolbar()

        if self.crop_overlay.superview:
            self.remove_subview(self.crop_overlay)

        self._render_edit_preview()
        self._update_edit_label()
        self.layout()

    # -- Actions -----------------------------------------------------------

    def pick_image(self, sender):
        """Open the iOS photo picker and load the selected image.

        Detects the original file format (HEIC, JPEG, PNG) from the
        asset filename and stores it for later export.

        Parameters
        ----------
        sender : ui.Button
            The button that triggered the action.
        """
        asset = photos.pick_asset()
        if not asset:
            return
        img = asset.get_image()
        if not img:
            return

        fname = getattr(asset, 'filename', '') or ''
        stem, orig_ext = os.path.splitext(fname)
        self._img_name = stem or 'photo'
        orig_ext = orig_ext.lstrip('.').upper()
        if orig_ext in ('HEIC', 'HEIF'):
            self._img_fmt = 'HEIC'
        elif orig_ext in ('JPG', 'JPEG'):
            self._img_fmt = 'JPEG'
        elif orig_ext == 'PNG':
            self._img_fmt = 'PNG'
        else:
            self._img_fmt = getattr(img, 'format', None) or 'PNG'

        self.raw_img = img
        self.thumb_img = self._thumb(img)
        self.baked_img = None
        self.rotation_angle = 0.0
        self.slices = []
        self.save_btn.alpha = 0
        self.page_label.text = ''
        for sv in list(self.scroll.subviews):
            self.scroll.remove_subview(sv)
        self.canvas.set_image(self._to_ui(self.thumb_img))
        self._update_edit_label()
        console.hud_alert(f'Loaded {self._img_fmt} \u2014 rotate, then Crop')

    def rotate_90(self, sender):
        """Increment the rotation angle by 90 degrees.

        Parameters
        ----------
        sender : ui.Button
            The button that triggered the action.
        """
        if not self.raw_img:
            return
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self._render_edit_preview()
        self._update_edit_label()

    def reset_angle(self, sender):
        """Reset the rotation angle to zero.

        Parameters
        ----------
        sender : ui.Button
            The button that triggered the action.
        """
        if not self.raw_img:
            return
        self.rotation_angle = 0.0
        self._render_edit_preview()
        self._update_edit_label()
        console.hud_alert('Reset')

    def do_slice(self, sender):
        """Slice the baked image into two 1080x1350 carousel frames.

        Uses the crop frame position and scale from ``CropOverlay`` to
        determine the pixel region, then splits it in half. Each half
        is resized to 1080x1350 (Instagram's optimal 4:5 size).

        Parameters
        ----------
        sender : ui.Button
            The button that triggered the action.
        """
        if not self.baked_img:
            return
        iw, ih = self.baked_img.size
        region = self.crop_overlay.crop_pixels(iw, ih)
        if not region:
            return
        cx, cy, cw, ch = region
        half = cw // 2
        if half < 1 or ch < 1:
            console.hud_alert('Crop area too small')
            return

        cx = max(0, min(cx, iw - cw))
        cy = max(0, min(cy, ih - ch))

        self.slices = []
        for sv in list(self.scroll.subviews):
            self.scroll.remove_subview(sv)

        scr_w = self.scroll.width
        scr_h = self.scroll.height
        self.scroll.content_size = (scr_w * 2, 0)

        for i in range(2):
            left = cx + i * half
            crop = self.baked_img.crop((left, cy, left + half, cy + ch))
            crop = crop.resize((1080, 1350), Image.LANCZOS)
            self.slices.append(crop)
            iv = ui.ImageView(frame=(i * scr_w, 0, scr_w, scr_h))
            iv.image = self._to_ui(crop)
            iv.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
            self.scroll.add_subview(iv)

        self.save_btn.alpha = 1
        self.page_label.text = '1 / 2'
        console.hud_alert('2 slices ready \u2014 1080\u00d71350 each')

    @ui.in_background
    def save_slices(self, sender):
        """Save slices to the Camera Roll in the original file format.

        Files are named ``{original_name}_car_1.{ext}`` and
        ``{original_name}_car_2.{ext}``. Falls back to JPEG if HEIC
        writing is not available.

        Parameters
        ----------
        sender : ui.Button
            The button that triggered the action.
        """
        if not self.slices:
            return
        console.show_activity()

        fmt = self._img_fmt.upper()
        heic_wanted = fmt in ('HEIC', 'HEIF')

        if heic_wanted and HAS_HEIF:
            ext, pil_fmt, save_kw = 'heic', 'HEIC', {'quality': 100}
        elif fmt == 'JPEG':
            ext, pil_fmt, save_kw = 'jpg', 'JPEG', {'quality': 100, 'subsampling': 0}
        elif fmt == 'PNG':
            ext, pil_fmt, save_kw = 'png', 'PNG', {}
        else:
            ext, pil_fmt, save_kw = 'jpg', 'JPEG', {'quality': 100, 'subsampling': 0}

        if heic_wanted and not HAS_HEIF:
            pil_fmt, ext = 'JPEG', 'jpg'
            save_kw = {'quality': 100, 'subsampling': 0}

        base = self._img_name
        try:
            tmp_dir = tempfile.mkdtemp()
            for i, s in enumerate(self.slices):
                out = s.convert('RGB') if pil_fmt == 'JPEG' else s
                name = f'{base}_car_{i+1}.{ext}'
                path = os.path.join(tmp_dir, name)
                out.save(path, format=pil_fmt, **save_kw)
                photos.create_image_asset(path)
                os.remove(path)
            os.rmdir(tmp_dir)
            console.hide_activity()
            label = pil_fmt
            if heic_wanted and not HAS_HEIF:
                label = 'JPEG (HEIC unavailable)'
            console.hud_alert(
                f'Saved {base}_car_1/2 as {label}!', 'success')
        except Exception as e:
            console.hide_activity()
            print(f'Error: {e}')
            console.hud_alert('Save failed')


if __name__ == '__main__':
    v = PanoramaPro()
    v.present('full_screen')
