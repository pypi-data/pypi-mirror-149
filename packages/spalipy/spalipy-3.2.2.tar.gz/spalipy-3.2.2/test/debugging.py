from test_spalipy import *
import logging
import matplotlib.pyplot as plt
from astropy.visualization import simple_norm

logging.getLogger().setLevel(logging.INFO)
template_data, template_dets = generate_image(seed=0)
source_data_footprint, source_dets_footprint = generate_image(
    translate=(13.2, -10), rotate=0, scale=1.0, seed=0
)
sp = Spalipy(
    source_data_footprint,
    template_data=template_data,
    min_n_match=10,
    sub_tile=1,
    spline_order=0,
    preserve_footprints=True,
)
sp.align()


fig, axes = plt.subplots(1, 4, figsize=(10, 5), sharex=True, sharey=True)
axes = axes.ravel()
norm = simple_norm(template_data, percent=99.5)
axes[0].imshow(source_data_footprint, cmap="viridis", norm=norm)
axes[0].set_title("Source")
axes[1].imshow(template_data, cmap="viridis", norm=norm)
axes[1].set_title("Template")
if sp.template_data is None:
    axes[2].imshow(np.zeros_like(template_data), cmap="viridis", norm=norm)
else:
    axes[2].imshow(sp.template_data, cmap="viridis", norm=norm)
axes[2].set_title("Template padded")
axes[3].imshow(sp.aligned_data, cmap="viridis", norm=norm)
axes[3].set_title(f"Spalipy aligned source")
plt.show()
