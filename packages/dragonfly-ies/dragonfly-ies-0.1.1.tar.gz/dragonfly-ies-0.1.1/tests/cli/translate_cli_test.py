import os

from click.testing import CliRunner

from ladybug.futil import nukedir

from dragonfly_ies.cli.translate import model_to_gem


def test_df_model_to_ies():
    runner = CliRunner()
    input_df_model = './tests/assets/simple_model.dfjson'
    folder = './tests/assets/temp'
    name = 'cli_df_model'

    result = runner.invoke(
        model_to_gem, [input_df_model, '--folder', folder, '--name', name]
    )
    assert result.exit_code == 0
    assert os.path.isfile(os.path.join(folder, f'{name}.gem'))
    nukedir(folder, True)


def test_invalid_df_model_to_ies():
    runner = CliRunner()
    input_df_model = './tests/assets/model_invalid_adj.dfjson'
    folder = './tests/assets/temp'
    name = 'cli_invalid_df_model'

    result = runner.invoke(
        model_to_gem,
        [input_df_model, '--folder', folder, '--name', name, '--bypass-adj-check']
    )
    assert result.exit_code == 0
    assert os.path.isfile(os.path.join(folder, f'{name}.gem'))
    nukedir(folder, True)
