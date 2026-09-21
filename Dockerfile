# Debian 13 "trixie" is the current Debian stable release
# the slim variant keeps the image small
FROM python:3.12-slim-trixie

# Pin GitHub Copilot CLI to latest release
ARG COPILOT_CLI_VERSION=1.0.83

# Non-root development user — declared as build args so they can be overridden
# (e.g. to match a host UID/GID) without editing the Dockerfile.
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Prevent pip from writing __pycache__ and from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# --- System packages, GitHub CLI, and Copilot CLI ---------------------------------
# Everything below runs as a single RUN so that install-time-only tooling (curl) can
# be purged again inside the very same layer, instead of leaving it in the image (and
# in an earlier layer other tools couldn't remove) just to satisfy "additional
# utilities needed for installation only".
#
#   ca-certificates : needed permanently — git, gh, pip, and copilot all speak HTTP and need a trust store to verify certificates.
#   curl            : needed only to (a) fetch gh's apt signing key and (b) fetch the Copilot CLI install script; removed at the end of this layer.
#   git             
#   gh              installed from GitHub's own apt repo so it tracks GitHub's signed releases rather than Debian's (often older) packaged version.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl; \
    \
    # GitHub CLI: add GitHub's official apt repo + signing key, then install `gh`.
    # This is GitHub's documented Debian/Ubuntu install method.
    install -d -m 0755 /etc/apt/keyrings; \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        -o /etc/apt/keyrings/githubcli-archive-keyring.gpg; \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends git gh; \
    \
    # GitHub Copilot CLI: use the official install script, pinned to an explicit
    # release tag via VERSION= (documented at https://github.com/github/copilot-cli),
    # instead of `npm install -g @github/copilot@latest` or the `@prerelease` tag.
    # This avoids adding a Node.js runtime just to run Copilot: the install script
    # fetches a self-contained platform binary from GitHub Releases.
    curl -fsSL https://gh.io/copilot-install \
        | VERSION="v${COPILOT_CLI_VERSION}" PREFIX="/usr/local" bash; \
    \
    # Record the resolved, actually-installed version for auditability, so anyone
    # inspecting a running container (or `docker history`) can see exactly what
    # shipped, independent of what the ARG default later drifts to.
    copilot --version | tee /etc/copilot-cli-version; \
    \
    # Drop the install-time-only tool and apt's package lists to keep the image small
    # and to avoid leaving a network client with no further job in the final image.
    apt-get purge -y --auto-remove curl; \
    rm -rf /var/lib/apt/lists/*

# Non-root development user
RUN groupadd --gid "${USER_GID}" "${USERNAME}" \
    && useradd --uid "${USER_UID}" --gid "${USER_GID}" --create-home --shell /bin/bash "${USERNAME}"

# Workspace
# /workspace is where a repo would be bind-mounted at `docker run` time
RUN mkdir -p /workspace && chown "${USERNAME}:${USERNAME}" /workspace
WORKDIR /workspace

USER ${USERNAME}

CMD ["/bin/bash"]