# ABNT Word Styles

This Macro is intented to create programaticaly througout VBA the Microsoft Word Styles and table of content as stablished in ABNT.

## Instalation procedure


### 1. Importing the modules

Open the Microsoft Word, in the ```Developer``` tab open the Visual Basic Editor and perform the following steps:

1. Import and run the module ```00_importModules.bas```;
2. When asked point the folder ```ABNT_Word_styles```;
3. Run the module ```a1_mainScript```;

### 2. Adjusting the indentation

1. Copy and paste to you document the text from the file ```sample_text.txt```;
2. Select all the text and format it with the style ```Text_body```.
3. Hit ```return``` twice in the keyboard to add two empty lines at the before the text;
4. From the tab ```Insert``` add a page break;
5. For each line in the sample text apply it respective style;
6. Adjust the indentation (if needed);
7. In the Microsoft Word windown, right click the following styles and uncheck the option ```Automatically update```:

        a. New_normal;

        b. Text_body;

        c. Title_unnumbered;

        d. Title_outside_TOC;

        e. Title_1;

        f. Title_2;

        g. Title_3;

        h. Title_4; and

        i. Title_5.

### 3. Generating the TOC

In the first line above the page break:

1. Type ```Sumário```, format it as ```Tittle_unnumbered```;
2. Run the macro ```Tool_createUserForm```;
3. Run the  macro ```a2_addToc```;
4. Select the level you want in TOC;
5. Adjust the TOC indentations; and
6. Save your file. Note that you'll be asked if you want to save the document as macro free document. Confirm the choice.