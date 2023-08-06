# MedicalImage

rm -r build dist medical_image.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*
