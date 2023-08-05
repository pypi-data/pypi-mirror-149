module.exports = {
  content: ["**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter var"],
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            h1: {
              fontWeight: 300,
              color: theme("colors.slate.500")
            },
            h2: {
              fontWeight: 300,
            },
            h3: {
              fontWeight: 600,
            },
            "dt:not(.sig)": {
              fontWeight: 600,
            },
            dt: {
              marginTop: "0.5em",
              marginBottom: "0.5em",
            },
            dd: {
              paddingLeft: "1.625em",
              marginTop: "0.5em",
              marginBottom: "0.5em",
            },
            "blockquote p.attribution::after": {
              content: "no-close-quotes",
            },
            "blockquote p:has(+ p.attribution)::after": {
              content: "close-quote",
            },
            "blockquote p.attribution": {
              fontSize: "0.875rem",
            },
            "blockquote.highlights": {
              fontStyle: "unset",
            },
            "blockquote.highlights p::before": {
              content: "no-open-quote",
            },
            "blockquote.highlights p::after": {
              content: "no-close-quote",
            },
            "td a.reference code.xref": {
              fontSize: 'inherit',
            },
            "td a.reference code.xref::before": {
              content: 'no-open-quote',
            },
            "td a.reference code.xref::after": {
              content: "no-close-quote",
            },
            "td > :first-child": {
              marginTop: 0,
            },
            "td > :last-child": {
              marginBottom: 0,
            },
            "li > :first-child": {
              marginTop: 0,
            },
            "li > :last-child": {
              marginBottom: 0,
            },
            "pre": {
              "--tw-prose-bold": "var(--tw-prose-pre-code)",
              "--tw-prose-links": "var(--tw-prose-pre-code)",
            }
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
  ],
}