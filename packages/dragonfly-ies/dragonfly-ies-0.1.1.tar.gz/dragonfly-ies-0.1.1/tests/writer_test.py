import pathlib
from dragonfly_ies.writer import model_to_ies
from dragonfly.model import Model


def test_df_model():
    in_file = './tests/assets/university_campus.dfjson'
    out_folder = pathlib.Path('./tests/assets/temp')
    out_folder.mkdir(parents=True, exist_ok=True) 
    model = Model.from_file(in_file)
    outf = model_to_ies(model, out_folder.as_posix(), name='uni_model')
    assert outf.exists()
