language: python
python:
- '3.7'
install:
- pip install -r requirements-travis.txt
script:
- python manage.py test
deploy:
  provider: heroku
  api_key:
    secure: hZmZuAML1eduDUJ5fjHYfXyS/bk5I3IRK1iuyTZYtxJnOnlAQoDdkpjdX19Jq2KtQwhURCY8RU9Uzwpw15IYf3Uqkph2iwOyxsi7gqmW7pvzmxVOULMNnNFamCs5cgL/cZEdW8Cktftat9pk4b833oM+Je+XKCHliHEbGbgnWatGKIuu2NCm4cWMHRoBSsPJ1qW+CagHHFxH8/KCvUo48/Gk3+8RdJCTcDD4lYaZlnScVddrTLn8Uxovnr54j+7s1CfdC0hlbJ67CFyaVlQIs7vhM9NJkMdjhH7GnXFy0qLZOhMyMwaenayfFw7BSnqOaCzDSTG2HEV9TmNvPmvwJaqEVzivU5jthFjC0K2TY/8LBT7HPv3o9yPxt/+j1z6VcPX8Df/pQ/BO1qnmToeESiq8k06Hh2Us8KhJIdCPe/yIj1JUujKWR4tfIJMZPy9FFp4ULIffYRrERrAhoVh/7tvqQ1BoXrn6qHh/nbQetHSPRN0xyoKQ8E8YnVytG5jYdHXki1sMBrkAG4vRXoEH1+hkOoH+5TEV/cS0cY9/a+Tkm8gVQ8GXI7wwXWge/M03j2CcmToiZFTFl/hyzK8HT5wNgtHXB5/nsVumAeFwAKfh2RP+9pS7ppba8VB9PXK7Xz7aaCgJIOl5n7zdd3Ohok3O5ecAP9JBi7fkyaUDWzc=
  app: project-102-code_crkrs
  on:
    repo: uva-cs3240-s20/project-102-code_crkrs
