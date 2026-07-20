# DOI and release strategy

## Companion book

Reserved DOI: **10.5281/zenodo.21459117**

This identifier belongs to the book *Engineering Trustworthy Crisis Intelligence*.

## Software

The repository should receive a separate Zenodo DOI after the first stable GitHub release. Recommended sequence:

1. connect the GitHub repository to Zenodo;
2. create a signed or annotated Git tag such as `v0.1.0`;
3. publish the GitHub release;
4. verify the generated Zenodo software record;
5. add the software DOI badge to the README and `CITATION.cff`;
6. relate the software and book records using `isSupplementTo` / `isSupplementedBy` as appropriate.

Never use the book DOI as though it identifies a particular software release.
