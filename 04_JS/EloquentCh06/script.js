/*
  code to learn to code in JS
*/

class vector {
  constructor(x,y) {
    this._x = x;
    this._y = y;
  }

  get x() {return this._x}

  get y() {return this._y}

  set x(value) {this._x = value}

  set x(value) {this._y = value}

  // Add iteration to the object
  *[Symbol.iterator] () {
    yield this._x;
    yield this._y;
  }

  // Polymorphism, editing the String output
  toString() {
    return `Vetor[${this._x},${this._y}]`;
  }

  get modulo() {
    return Math.sqrt(
      Math.pow(this._x , 2) + Math.pow(this._y , 2)
    );
  }

  componentes() {
    return [this._x, this._y];
  }

  quadrado() {
    return this._x * this._x + this._y * this._y
  }

  add(another) {
    this._x = this._x + another.x;
    this._y = this._y + another.y;
    return this.toString();
  }

  subtract(another) {
    this._x = this._x - another.x;
    this._y = this._y - another.y;
    return this.toString();
  }

  unitario() {
    return [ this._x / this.modulo(), this._y / this.modulo() ];
  }
}

class Temperature {
  constructor(celsius) {
    this.celsius = celsius;
  }

  get fahrenheit() {
    return this.celsius * 1.8 + 32;
  }

  set fahrenheit(value) {
    this.celsius = (value - 32) / 1.8;
  }

  static fromFahrenheit(value) {
    return new Temperature((value - 32) / 1.8);
  }
}
