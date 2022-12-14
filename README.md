# Brilliant Docs - Source

This site is built with [Jekyll](https://jekyllrb.com) and [Just the Docs](https://github.com/just-the-docs/just-the-docs). It's all hosted here on GitHub using the GitHub's [Pages](https://pages.github.com) feature.

**If you spot any errors** in our documentation, feel free to make an [issue](https://github.com/Itsbrilliantlabs/docs/issues).

If you'd like to do some extensive editing, you can also fork/clone this repository and view the pages live editing.

## To set it up:

1. Ensure you have [Ruby installed](https://www.ruby-lang.org/en/documentation/installation/). On MacOS, ruby is already installed and ready to go.

1. Clone this repository:

    ```bash
    git clone https://github.com/Itsbrilliantlabs/docs.git
    ```

1. Set up the environment:

    ```bash
    cd docs
    bundle install
    ```

1. Open the project in your browser:

    ```bash
    bundle exec jekyll serve --livereload --open-url
    ```


That's it! As you edit the pages. The website will automatically refresh. Be sure to keep an eye on your terminal to spot any error messages while you're developing.