

# The following two methods allow you to display a suitable image format to the client,
# based on the browser and its version

### Version 1 python code
### Lib django-user-agents

### A lot of code, maybe not the best version

def check_use_webp(user_agent) -> bool:
    browser = user_agent.browser.family.lower()
    version = next(iter(user_agent.browser.version), 0)

    browser_version_exceptions = {'edge': 17, 'firefox': 64, 'chrome': 31, 'safari': 14,
                                  'opera': 18, 'android browser': 4.1, 'safari on ios': 13.7}

    if browser in browser_version_exceptions and version <= browser_version_exceptions[browser]:
        return False

    return True


### Version 2 html
### The picture tag itself substitutes the image for the user based on the browser and its version
### Not available on old versions of browsers and on the window explorer

    <picture>
      <source type="image/webp" srcset="{{ work.image_webp.url }}">
      <img  src="{{ work.image.url }}"/>
    </picture>