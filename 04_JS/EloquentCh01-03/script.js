/*
  code to learn to code in JS
*/
const square = x => x * x;

const printFizzBuzz = function() {
  for (let counter = 1; counter <= 100; counter += 1) {
    if (counter % 3 == 0 && counter % 5 == 0) {
      console.log('FizzBuzz');
    }
    else if (counter % 3 == 0) {
      console.log('Fizz');
    }
    else if (counter % 5 == 0) {
      console.log('Buzz');
    }
    else {
      console.log(counter);
    }
  }
}

const printBytesComb = function(qtd) {
  let total = 1;
  for (let counter = 1; counter <= qtd; counter += 1) {
    total = total * 2;
  }
  console.log("Number of possible combinations: " + total);
}

const printChessBoard = function(size) {
  let str = '';
  for (let rowCounter = 1; rowCounter <= size; rowCounter += 1){
    for (let colCounter = 1; colCounter <= (size/2); colCounter += 1) {
      if (rowCounter % 2 != 0){
        str = str + '#_';
      }
      else if (rowCounter % 2 == 0) {
        str = str + '_#';
      }
    }
    str = str + '\n';
  }
  console.log(str);
}

// fábrica de objetos
function createPeople(name, surname) {
  let person = {};
  person.name = name;
  person.surname = surname;

  const fullName = () => `${person.name} ${person.surname}`;

  person.fullName = fullName();
  return person;
}

let pessoaA = createPeople('Cristofer','Costa');

// optional arguments example
function minus(a,b) {
  if (b === undefined) return -a;
  else return a - b;
}

// recursion in functions -> slower then use simple loop
function power(base, exponent) {
  if (exponent == 0) return 1;
  else return base * power(base, exponent - 1);
}

function isEven(value) {
  if (value < 0) value = - value
  while (value > 1) value = value - 2
  if (value == 0) return true
  else return false
}
