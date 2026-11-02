"""
Testes automatizados para a Calculadora Python
Valida as 4 operações básicas, a nova operação de porcentagem,
o tratamento de exceções (como divisão por zero) e o histórico.
"""
import unittest
import calculadora as calc


class TestCalculadora(unittest.TestCase):
    def setUp(self):
        """Limpa o histórico antes de cada teste para isolar os cenários."""
        calc.limpar_historico()

    def test_somar(self):
        self.assertEqual(calc.somar(10, 5), 15)
        self.assertEqual(calc.somar(-2, 5), 3)
        self.assertEqual(calc.somar(0, 0), 0)
        self.assertEqual(calc.calcular(10, "+", 5), 15)

    def test_subtrair(self):
        self.assertEqual(calc.subtrair(20, 8), 12)
        self.assertEqual(calc.subtrair(5, 10), -5)
        self.assertEqual(calc.subtrair(0, 0), 0)
        self.assertEqual(calc.calcular(20, "-", 8), 12)

    def test_multiplicar(self):
        self.assertEqual(calc.multiplicar(6, 4), 24)
        self.assertEqual(calc.multiplicar(7, 0), 0)
        self.assertEqual(calc.multiplicar(-3, 3), -9)
        self.assertEqual(calc.calcular(6, "*", 4), 24)

    def test_dividir(self):
        self.assertEqual(calc.dividir(20, 4), 5)
        self.assertEqual(calc.dividir(7, 2), 3.5)
        self.assertEqual(calc.calcular(20, "/", 4), 5)

    def test_divisao_por_zero(self):
        """Verifica se o erro esperado é disparado ao dividir por zero."""
        with self.assertRaises(ZeroDivisionError):
            calc.dividir(10, 0)
        with self.assertRaises(ZeroDivisionError):
            calc.calcular(10, "/", 0)

    def test_porcentagem(self):
        """Valida o cálculo de porcentagem em diferentes cenários."""
        # 15% de 200 = 30
        self.assertEqual(calc.porcentagem(200, 15), 30)
        # 50% de 80 = 40
        self.assertEqual(calc.porcentagem(80, 50), 40)
        # 0% de qualquer número deve ser 0
        self.assertEqual(calc.porcentagem(500, 0), 0)
        # 100% de um número deve ser ele mesmo
        self.assertEqual(calc.porcentagem(45.5, 100), 45.5)
        # Teste através da função genérica 'calcular'
        self.assertEqual(calc.calcular(200, "%", 15), 30)

    def test_expressao_com_porcentagem(self):
        """Valida se expressões encadeadas avaliam a porcentagem corretamente."""
        # 100 + (200 % 10) = 100 + 20 = 120
        res = calc.calcular_expressao("100 + 200 % 10")
        self.assertEqual(res["resultado"], 120.0)

    def test_historico(self):
        """Garante que as operações continuam sendo registradas corretamente."""
        calc.calcular(10, "+", 5)
        calc.calcular(200, "%", 10)
        historico = calc.obter_historico()

        self.assertEqual(len(historico), 2)
        self.assertEqual(historico[0]["expressao"], "10 + 5")
        self.assertEqual(historico[0]["resultado"], "15")
        self.assertEqual(historico[1]["expressao"], "200 % 10")
        self.assertEqual(historico[1]["resultado"], "20")


if __name__ == "__main__":
    unittest.main(verbosity=2)
