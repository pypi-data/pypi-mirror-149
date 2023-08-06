# sphinx-rfcsection
`sphinx-rfcsection` is a minimal Sphinx extension to add sane automatic titles
to RFC references with sections included.

## Implementation details
For simplicity, this extension subclasses Sphinx's built-in `:rfc:` role from
`sphinx.roles.RFC` (part of the Sphinx code since version 2.x). Just a small
amount of custom logic automatically sets a custom title on the reference if
appropriate, before delegating right back to the built-in code.

## License
[GPLv3](https://opensource.org/licenses/GPL-3.0)
