let currentInput = '';
let currentOperator = '';
let firstOperand = null;
let historico = [];
let indexCalculo = 1;

const displayExpression = document.getElementById('expression');
const displayResult = document.getElementById('result');
const historyList = document.getElementById('history-list');

// Funções Matemáticas Base
const somar = (a, b) => a + b;
const subtrair = (a, b) => a - b;
const multiplicar = (a, b) => a * b;
const dividir = (a, b) => {
  if (b === 0) throw new Error("Não é possível dividir por zero.");
  return a / b;
};
const porcentagem = (a, b) => (a * b) / 100;

const OPERACOES = {
  '+': { fn: somar, nome: 'somar' },
  '-': { fn: subtrair, nome: 'subtrair' },
  '*': { fn: multiplicar, nome: 'multiplicar' },
  '/': { fn: dividir, nome: 'dividir' },
  '%': { fn: porcentagem, nome: 'porcentagem' }
};

function formatarNumero(val) {
  if (isNaN(val)) return 'Erro';
  if (Number.isInteger(val)) return val.toString();
  return Number(val.toFixed(8)).toString();
}

function appendNum(num) {
  if (num === '.' && currentInput.includes('.')) return;
  currentInput += num;
  updateDisplay();
}

function appendOp(op) {
  if (currentInput === '' && firstOperand === null) return;

  if (firstOperand !== null && currentInput !== '') {
    calculate();
  }

  if (currentInput !== '') {
    firstOperand = parseFloat(currentInput);
    currentInput = '';
  }

  currentOperator = op;
  updateDisplay();
}

function calculate() {
  if (firstOperand === null || currentInput === '' || !currentOperator) return;

  const secondOperand = parseFloat(currentInput);
  const opInfo = OPERACOES[currentOperator];
  const now = new Date();
  const horario = now.toTimeString().split(' ')[0];

  const exprStr = `${formatarNumero(firstOperand)} ${currentOperator} ${formatarNumero(secondOperand)}`;
  const pythonStr = `${opInfo.nome}(${formatarNumero(firstOperand)}, ${formatarNumero(secondOperand)})`;

  try {
    const resValue = opInfo.fn(firstOperand, secondOperand);
    const resFormatted = formatarNumero(resValue);

    displayResult.innerText = resFormatted;
    displayExpression.innerText = `${exprStr} =`;

    // Salva no histórico
    adicionarAoHistorico({
      indice: indexCalculo++,
      horario: horario,
      expressao: exprStr,
      python: pythonStr,
      resultado: resFormatted
    });

    firstOperand = resValue;
    currentInput = '';
    currentOperator = '';
  } catch (error) {
    displayResult.innerText = 'Erro';
    displayExpression.innerText = error.message;

    adicionarAoHistorico({
      indice: indexCalculo++,
      horario: horario,
      expressao: exprStr,
      python: pythonStr,
      resultado: 'ZeroDivisionError'
    });

    firstOperand = null;
    currentInput = '';
    currentOperator = '';
  }
}

function clearAll() {
  currentInput = '';
  currentOperator = '';
  firstOperand = null;
  displayResult.innerText = '0';
  displayExpression.innerText = '';
}

function deleteLast() {
  currentInput = currentInput.slice(0, -1);
  updateDisplay();
}

function updateDisplay() {
  if (currentInput !== '') {
    displayResult.innerText = currentInput;
  } else if (firstOperand !== null) {
    displayResult.innerText = formatarNumero(firstOperand);
  } else {
    displayResult.innerText = '0';
  }

  if (firstOperand !== null && currentOperator) {
    displayExpression.innerText = `${formatarNumero(firstOperand)} ${currentOperator}`;
  }
}

function adicionarAoHistorico(item) {
  historico.unshift(item);
  renderHistorico();
}

function renderHistorico() {
  if (historico.length === 0) {
    historyList.innerHTML = '<p class="empty-msg">Nenhum cálculo realizado ainda.</p>';
    return;
  }

  historyList.innerHTML = historico.map(item => `
    <div class="history-item">
      <div class="meta">
        <span>#${String(item.indice).padStart(2, '0')}</span>
        <span>${item.horario}</span>
      </div>
      <div class="calc-expr">${item.expressao} = <strong>${item.resultado}</strong></div>
      <div class="calc-python">${item.python}</div>
    </div>
  `).join('');
}

function clearHistory() {
  historico = [];
  indexCalculo = 1;
  renderHistorico();
}

// Suporte a teclado
document.addEventListener('keydown', (e) => {
  if (e.key >= '0' && e.key <= '9') appendNum(e.key);
  if (e.key === '.') appendNum('.');
  if (['+', '-', '*', '/', '%'].includes(e.key)) appendOp(e.key);
  if (e.key === 'Enter' || e.key === '=') calculate();
  if (e.key === 'Backspace') deleteLast();
  if (e.key === 'Escape') clearAll();
});