# Contribution Guidelines

## Contributing

Contributions to Squishy are released under the following licenses depending on the component:

* [CERN-OHL-S] - Hardware
* [CC-BY-SA] - Documentation

Please note that Squishy is released with a [Contributor Code of Conduct]. By participating in this project you agree to abide by its terms.

## Development and Testing

Prior working on squishy, ensure you understand have have followed the general [Installation] guide, when installing Squishy make sure to add `[dev]` do the package name to ensure the needed development tools are installed along with squishy.

Alternatively, use `pip` to install [nox], like so:

```
$ pip install nox
```

General testing and linting of Squishy is done with nox, as such there are some session names to know about:

* `test` - Run the test suite
* `lint` - Run the linter
* `typecheck` - Run the type-checker

Bye default these are configured to run one right after another when invoking `nox` with no arguments, to run a single check, you can run it with passing `-s <session>` to nox, like so:

```
$ nox -s lint
```

In addition to this, to work on the hardware, you need a copy of [KiCad] 9.0 or newer.

## Use of Generative AI

This project explicitly does not allow any contributions that were generated in whole or in-part by large language models (LLMs), chatbots, or image generation systems. This ban includes tools, including but not limited to Copilot, ChatGPT, Claude, DeepSeek, Stable Diffusion, DALL-E, Midjourney, or Devin AI.

This policy covers all parts of the project, including, but not limited to code, documentation, issues, artworks, comments, discussions, pull requests, and any other contributions to Squishy, without exception.

> [!NOTE]
> It is also recommended to avoid any and all AI tools when asking questions about Squishy,
> prefer the documentation when available, as well as things such as the discussion forum, or IRC channel.
> These tools often fabricate plausible sounding information that is entirely incorrect, or often subtly
> incorrect and pass it off with confidence, thus misleading.

[CERN-OHL-S]: ./LICENSE
[CC-BY-SA]: https://github.com/squishy-scsi/squishy/blob/main/LICENSE.docs
[Contributor Code of Conduct]: ./CODE_OF_CONDUCT.md
[Installation]: https://docs.scsi.moe/install.html
[nox]: https://nox.thea.codes/
[KiCad]: https://www.kicad.org/
