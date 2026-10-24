
from pathlib import Path   # pathlib is a Python module used for working with files and folders (directories).

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


# 1. Project settings
SIZE = 64
SAMPLING_FRACTION = 0.30
NOISE_SIGMA = 0.01
SEED = 7

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

rng = np.random.default_rng(SEED)


# 2. Create a synthetic radio sky
def make_sky(size):
    sky = np.zeros((size, size))

    sources = [
        (12, 15, 1.0),
        (20, 44, 0.8),
        (36, 18, 0.7),
        (47, 48, 0.9),
        (29, 32, 0.6),
        (51, 12, 0.55),
        (14, 51, 0.65),
        (41, 35, 0.75),
    ]

    for row, col, brightness in sources:
        sky[row, col] = brightness

    sky = gaussian_filter(sky, sigma=0.8)
    sky /= sky.max()

    return sky


# 3. Fourier transform functions
def fft2(image):
    return np.fft.fft2(image, norm="ortho")


def ifft2(frequencies):
    return np.fft.ifft2(frequencies, norm="ortho")


# 4. Generate a Fourier sampling mask
def make_mask(size, fraction, random_generator):
    mask = random_generator.random((size, size)) < fraction

    # Keep the zero-frequency measurement.
    mask[0, 0] = True

    # Enforce conjugate symmetry for real-valued images.
    negative_indices = (-np.arange(size)) % size
    mirrored = mask[np.ix_(negative_indices, negative_indices)]
    mask = mask | mirrored

    return mask.astype(float)


# 5. Simulate incomplete and noisy measurements
def simulate_measurements(sky, mask, noise_sigma, random_generator):
    clean_measurements = mask * fft2(sky)

    noise = (
        random_generator.normal(size=sky.shape)
        + 1j * random_generator.normal(size=sky.shape)
    ) / np.sqrt(2.0)

    return clean_measurements + mask * noise_sigma * noise


# 6. Reconstruct using zero-filled inverse FFT
def reconstruct_zero_filled(measurements, mask):
    image = np.real(ifft2(mask * measurements))
    return np.maximum(image, 0.0)


# 7. Run the experiment
def main():
    sky = make_sky(SIZE)
    mask = make_mask(SIZE, SAMPLING_FRACTION, rng)

    measurements = simulate_measurements(
        sky, mask, NOISE_SIGMA, rng
    )

    reconstruction = reconstruct_zero_filled(measurements, mask)

    relative_error = (
        np.linalg.norm(reconstruction - sky)
        / np.linalg.norm(sky)
    )
    mse = np.mean((reconstruction - sky) ** 2)

    psnr = 10 * np.log10(1.0 / mse)


    print(f"Image size: {SIZE} x {SIZE}")
    print(f"Sampling fraction: {mask.mean():.2%}")
    print(f"Relative reconstruction error: {relative_error:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.6f}")
    print(f"Peak Signal-to-Noise Ratio (PSNR): {psnr:.2f} dB")

    # Plot the sky, mask and reconstruction.
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    axes[0].imshow(sky, cmap="magma")
    axes[0].set_title("Ground-truth sky")

    axes[1].imshow(mask, cmap="gray")
    axes[1].set_title("Fourier sampling mask")

    axes[2].imshow(reconstruction, cmap="magma")
    axes[2].set_title("Zero-filled reconstruction")

    for axis in axes:
        axis.axis("off")

    fig.tight_layout()
    fig.savefig(RESULTS / "first_reconstruction.png", dpi=160)
    plt.show()

    print(f"Image saved to: {RESULTS / 'first_reconstruction.png'}")


if __name__ == "__main__":
    main()
