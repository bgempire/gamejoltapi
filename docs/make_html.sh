rm *.html
rm -r _static
make html
mv _build/html/* ./
rm -r _build/
rm -r _sources/
