# After modifying, run `bundle update`, then `bundle install`
# Then, star the sit with: `bundle exec jekyll serve --livereload --open-url``

source "https://rubygems.org"

gem "github-pages", "~> 228", group: :jekyll_plugins

group :jekyll_plugins do
  gem 'jekyll-include-cache', "~> 0.2.1"
  gem "jekyll-redirect-from", "~> 0.16.0"
  gem "jekyll-seo-tag", "~> 2.8.0"
  gem "jekyll-sitemap", "~> 1.4.0"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data
# gem and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
