# Contributing to Orrery Labs

Thank you for helping. A good lab teaches one real skill well, and it is honest about what it leaves out.

## Proposing a lab

Open an issue using the **Lab proposal** form. Say who the lab is for, what they will be able to do afterwards, and how a second person would check the result.

## Writing or improving a lab

1. Fork the repository and create a branch.
2. Copy `labs/_template/` to `labs/NN-short-name/` and fill in every section.
3. Use synthetic data only. Never commit real names, records, credentials or private documents.
4. Run `python tools/check_labs.py`. It must print `PASS`.
5. Open a pull request. A maintainer reviews every change before it merges.

## Licensing of contributions

By contributing, you agree that your code is released under the [MIT License](LICENSE) and your written content under [CC BY 4.0](LICENSE-CONTENT), the same terms as the rest of the repository.
