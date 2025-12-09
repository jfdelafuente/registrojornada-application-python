import pytest
from datetime import datetime
from io import StringIO
from app.main import main


@pytest.mark.parametrize(
    "args, expected_output",
    [
        (
            ["script_name.py"],
            "Error: Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]",
        ),
        (
            ["script_name.py", "INVALID_ARGUMENT"],
            "Error: Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]",
        ),
        (["script_name.py", "INFOP"], "Argumento de entrada: INFOP"),
    ],
)
def test_main_no_argument(args, expected_output, capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(args)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output


def test_main_dia_argument():
    args = ["script_name.py", "DIA", "YYMMDD"]
    with StringIO() as fake_out:
        main(args)
        assert (
            fake_out.getvalue().strip()
            == "MAIN - Enviando mensaje: 'Mensaje de registro' con exito."
        )


# def test_main_notificar_true(monkeypatch):
#     args = ["script_name.py", "DIA", "YYMMDD"]
#     monkeypatch.setattr('api.ViveOrange.ViveOrange.registrar', lambda *args, **kwargs: "Mensaje de registro")
#     monkeypatch.setattr('api.BotTelegramRegistro.BotTelegramRegistro.send_to_telegram_dummy', lambda *args, **kwargs: True)
#     with StringIO() as fake_out:
#         main(args)
#         assert fake_out.getvalue().strip() == "MAIN - Enviando mensaje: 'Mensaje de registro' con exito."

# def test_main_send_to_telegram_failure(monkeypatch):
#     args = ["script_name.py", "DIA", "YYMMDD"]
#     monkeypatch.setattr('api.ViveOrange.ViveOrange.registrar', lambda *args, **kwargs: "Mensaje de registro")
#     monkeypatch.setattr('api.BotTelegramRegistro.BotTelegramRegistro.send_to_telegram_dummy', lambda *args, **kwargs: False)
#     with StringIO() as fake_out:
#         main(args)
#         assert fake_out.getvalue().strip() == "Error al enviar el mensaje."
