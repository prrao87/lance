# Lance Documentation

This directory contains the documentation for Lance, built with Zensical.

## Getting Started with uv

### Setup

1. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. That's it! No manual dependency installation needed.

### Building Documentation

Use Zensical’s official commands (`build`, `serve`) with a required protobuf pre-render step.

To build and preview locally:

```bash
UV_CACHE_DIR=.uv-cache uv sync --all-extras
python3 tools/render_proto_macros.py --input src --output .generated/src
uv run zensical build --clean -f zensical.toml
uv run zensical serve -f zensical.toml -a localhost:8000
```

The documentation will be available at http://localhost:8000

### Building for Production

```bash
python3 tools/render_proto_macros.py --input src --output .generated/src
uv run zensical build --clean -f zensical.toml
```

This will create a `site/` directory with the built documentation.

If you prefer convenience wrappers, `make serve` and `make build` run the same sequence.

To run the current Zensical-only validation pass:

```bash
make check-links
```

To preview the static output from `site/`:

```bash
python3 -m http.server 4173 --directory site
```

## Deploying on a Fork with GitHub Pages

The repository includes a Pages workflow at
`/.github/workflows/docs-deploy.yml` that builds with Zensical and deploys via
`actions/deploy-pages`.

Before first deploy on a fork:

1. In GitHub, go to `Settings -> Pages` and set `Source` to `GitHub Actions`.
2. Ensure Actions are enabled for the fork (`Settings -> Actions -> General`).
3. Trigger `publish-site` once from `Actions -> publish-site -> Run workflow`
   (or push to `main`).
4. After the run completes, use the `github-pages` environment URL shown in the
   deploy job summary.

The deployed URL for forks is the default GitHub Pages URL
(`https://<owner>.github.io/<repo>/`) unless you later add a custom domain.

### Managing Dependencies

#### Adding Dependencies

```bash
# Add a dependency and update pyproject.toml
uv add <package>

# Add a dev dependency
uv add --dev <package>
```

#### Manual Sync (if needed)

```bash
make sync
```

#### Upgrading Dependencies

```bash
# Upgrade a specific package
uv add <package>@latest

# Upgrade all dependencies
uv sync --upgrade
```

## Project Structure

- `src/` - Source markdown files for documentation
- `tools/render_proto_macros.py` - Pre-renders protobuf macros into generated markdown
- `zensical.toml` - Zensical configuration
- `pyproject.toml` - Python project configuration (uv compatible)
