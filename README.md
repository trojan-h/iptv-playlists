 # DE + IT + IL EPG bundle for GitHub

This bundle creates a combined XMLTV EPG file from:

- https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz
- https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz
- https://epgshare01.online/epgshare01/epg_ripper_IL1.xml.gz

## How to use

1. Create a public GitHub repository.
2. Upload all files from this bundle to the repository root.
3. Go to **Settings → Pages** and enable GitHub Pages from the **main** branch, root folder.
4. Go to **Actions** and run the workflow once, or wait for the scheduled run.
5. Your combined EPG will be published as:

   `https://<YOUR_GITHUB_USERNAME>.github.io/<YOUR_REPO_NAME>/epg_de_it_il.xml.gz`

Use that URL in IPTVX under **Settings → EPG Sources**.

## Notes

- The workflow runs every day and also on manual trigger.
- The output file is plain XMLTV merged from the three source files.
- The script keeps all channels and programmes from DE, IT, and IL.
