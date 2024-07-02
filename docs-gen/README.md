# VSS Documentation

The VSS documentation is realized with GitHub Pages. It is generated from
the markdown files in the ```/docs-gen``` directory of this repository.
The static webpage is generated automatically after every PR merged to master
and deployed into a branch called `gh-pages`.

## Known limitations

Links in this folder are typically not possible to follow in Github as they refer to position in the generated documentation
rather than in source documentation. That could possibly be solved by [Hugo Render Hooks](https://gohugo.io/templates/render-hooks/)
but it is not trivial to get a solution that works for all types of internal links.

## How to link internally

We generally use "Hugo-style links" like `/vehicle_signal_specification/governance/`.
They do not work when viewing documentation in Github but are the easiest to use for safe documentation generation.

Some guidelines:

* To link to a file like `rule_set/overlay.md` use `/vehicle_signal_specification/rule_set/overlay/`
* To link to an index file like `rule_set/_index.md` use `/vehicle_signal_specification/rule_set/`
* To link to a picture like `static/images/taxonomies.png` use `/vehicle_signal_specification/images/taxonomies.png`

Never link directly to a specific page at `github.io` - in the future we might want to keep multiple versions of
documentation and then links must go to the correct version.

## Verifying links

We can use `markdown-link-check` to check markdown files. It can be installed like this

```
sudo apt install nodejs npm
sudo npm install -g markdown-link-check
```

What to run:
```
cd vehicle_signal_specification
markdown-link-check *.md
markdown-link-check vss-tools/*.md
markdown-link-check vss-tools/docs/*.md
```

For generated files (Hugo) links can be checked with [W3C Link Checker](https://validator.w3.org/checklink), running
on `https://covesa.github.io/vehicle_signal_specification/`. It checks against latest master.
Run check with `Check linked documents recursively`


## Dependencies

The static page is generated with:

- [HUGO](https://gohugo.io/)
- [Learn Theme](https://github.com/matcornic/hugo-theme-learn)

Please follow the [documentation](https://gohugo.io/documentation/) for installation and further questions around the framework.
Currently, the HUGO version used for generating VSS documentation is `0.103.1`,
as controlled by the [buildcheck.yml](https://github.com/COVESA/vehicle_signal_specification/blob/master/.github/workflows/buildcheck.yml)


## Run the documentation server locally

Once hugo is installed please follow the following steps:

### Check that HUGO is working:
```
hugo version
```
The following outcome is expected:

```
Hugo Static Site Generator v0.xx.xx ...
```

### Clone the submodule containing the theme

Run the following git commands to init and fetch the submodules:

```
git submodule init
git submodule update
```

Reference: [Git Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

### Test locally on your server:

Within the repository

```
hugo server -D -s ./docs-gen
```

Optional ```-D:``` include draft pages as well. Afterwards, you can access the
page under http://localhost:1313/vehicle_signal_specification.

## Contribute

If you want to contribute, do the following:

1. **Change documentation in ```/docs-gen```**

1. **Test your changes locally, as described above**

1. **Create Pull Request for review**
