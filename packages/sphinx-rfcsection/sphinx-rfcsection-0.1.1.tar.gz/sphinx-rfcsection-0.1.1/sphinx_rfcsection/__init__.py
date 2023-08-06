from sphinx.roles import RFC


class RFCWithSection(RFC):
    """RFC role that automatically titles section refs sanely."""
    def run(self):
        if not self.has_explicit_title and '#' in self.target:
            num, section = self.target.split('#', 1)
            try:
                section = float(section.replace('section-', ''))
            except ValueError:
                pass  # use it as-is
            else:
                section = str(section)

            self.title = 'RFC {} § {}'.format(num, section)
            self.has_explicit_title = True

        return super().run()


def setup(app):
    app.add_role('rfc', RFCWithSection(), override=True)

    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
