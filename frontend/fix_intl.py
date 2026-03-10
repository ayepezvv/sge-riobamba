path = "src/ui-component/Locales.tsx"
with open(path, "r") as f:
    content = f.read()

content = content.replace(
    '<IntlProvider locale={i18n} defaultLocale="en" messages={messages}>',
    '<IntlProvider locale={i18n} defaultLocale="es" messages={messages} onError={() => {}}>'
)

with open(path, "w") as f:
    f.write(content)
