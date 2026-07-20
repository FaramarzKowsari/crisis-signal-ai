# Google Search Console setup for CrisisSignal AI

## Property to add

Use a **URL-prefix property** with this exact address:

```text
https://faramarzkowsari.github.io/crisis-signal-ai/
```

Do not add the GitHub repository URL (`github.com/FaramarzKowsari/crisis-signal-ai`) as the project website property. Search Console should track the public GitHub Pages website.

Because the parent property `https://faramarzkowsari.github.io/` is already verified, Google may automatically verify this child URL-prefix property.

## Published indexing files

After the Documentation workflow succeeds, these files must be publicly accessible:

```text
https://faramarzkowsari.github.io/crisis-signal-ai/robots.txt
https://faramarzkowsari.github.io/crisis-signal-ai/sitemap.xml
```

The project uses:

- `docs/robots.txt` as the source for the live robots file;
- MkDocs, with `site_url` configured, to generate `sitemap.xml`;
- `scripts/validate_search_assets.py` to check both assets before deployment;
- `.github/workflows/docs.yml` to build, validate and deploy the site.

## Verification when auto-verification does not occur

Choose **HTML file upload** in Search Console and download the exact file provided by Google.

Do not rename or edit that file.

Extract the indexing package and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install_google_verification.ps1 `
  -TargetRepo "C:\Faramarz\GitHub\NLP-Disaste-Tweets-LSTM-Colorado" `
  -VerificationFile "C:\PATH\TO\googleXXXXXXXXXXXX.html"
```

Commit and push the new file in GitHub Desktop. After GitHub Pages deploys, open its expected URL in an Incognito window. Then return to Search Console and click **Verify**.

The verification file must remain in the repository. Google checks ownership periodically.

## Submit the sitemap

In Search Console:

1. Select the property:
   `https://faramarzkowsari.github.io/crisis-signal-ai/`
2. Open **Sitemaps**.
3. In **Add a new sitemap**, enter:

```text
sitemap.xml
```

4. Click **Submit**.

The submitted full address is:

```text
https://faramarzkowsari.github.io/crisis-signal-ai/sitemap.xml
```

## Request indexing

Use **URL Inspection** for these priority pages and click **Request indexing**:

```text
https://faramarzkowsari.github.io/crisis-signal-ai/
https://faramarzkowsari.github.io/crisis-signal-ai/author/
https://faramarzkowsari.github.io/crisis-signal-ai/doi-strategy/
https://faramarzkowsari.github.io/crisis-signal-ai/model-card/
https://faramarzkowsari.github.io/crisis-signal-ai/dataset-card/
https://faramarzkowsari.github.io/crisis-signal-ai/research-roadmap/
```

Submitting a sitemap and requesting indexing help Google discover the URLs, but they do not guarantee indexing.

## Final live checks

Open these URLs in a browser:

```text
https://faramarzkowsari.github.io/crisis-signal-ai/robots.txt
https://faramarzkowsari.github.io/crisis-signal-ai/sitemap.xml
```

The robots file must contain:

```text
User-agent: *
Allow: /

Sitemap: https://faramarzkowsari.github.io/crisis-signal-ai/sitemap.xml
```

The sitemap must list the project home page and all important documentation pages.
