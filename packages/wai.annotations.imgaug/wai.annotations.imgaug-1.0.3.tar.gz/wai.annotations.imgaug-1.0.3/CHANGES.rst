Changelog
=========

1.0.3 (2022-05-05)
------------------

- `--labels` option of the `add-annotation-overlay-od` plugin gets respected now,
  also using correct label for text now (when varying the colors)


1.0.2 (2022-05-05)
------------------

- added `add-annotation-overlay-od` plugin to overlay the object detections on the images


1.0.1 (2022-03-01)
------------------

- added more typing hints to parameters
- added ability to add augmented images rather than replace original ones, using
  the `-m/--mode add` option (`--suffix` overrides the default suffix)
- added `scale` ISP for scaling images


1.0.0 (2022-02-23)
------------------

- Initial release: crop, flip, gaussian-blur, hsl-grayscale, linear-contrast, rotate
