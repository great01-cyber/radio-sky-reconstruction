# Radio Sky Reconstruction
### A Simplified Example of Computational Imaging

## 1. Project Overview

Radio Sky Reconstruction is a small computational imaging project that explores how an image of the sky can be reconstructed from incomplete and noisy Fourier measurements.

In radio astronomy, telescopes do not always obtain a complete set of measurements needed to directly recover an image. Reconstruction algorithms are therefore used to estimate the original sky image from the available data.

This project uses a **synthetic radio-sky image** to demonstrate the basic principles behind this problem. It begins with a simple reconstruction method and will be extended to compare more advanced optimisation-based and Plug-and-Play methods.

The project is educational and research-oriented. It is not a complete radio telescope simulator and does not model the full physics or measurement process of a real radio interferometer.

## 2. Research Question

**How do different reconstruction algorithms perform when a radio telescope has only incomplete measurements of the sky?**

A more specific version of the research question is:

> How do optimisation-based and Plug-and-Play methods compare in reconstruction accuracy, data consistency, and convergence behaviour when recovering a synthetic radio-sky image from incomplete and noisy Fourier measurements?

### Supporting Questions

1. How accurately can a sky image be reconstructed when only a fraction of its Fourier measurements are available?
2. How does the reconstruction quality of a simple zero-filled inverse Fourier transform compare with that of FISTA and Plug-and-Play (PnP) methods?
3. How does the proportion of missing Fourier measurements affect reconstruction quality?
4. How do the algorithms behave over successive iterations, and do their reconstruction errors stabilise?

## 3. Project Objectives

The main objectives are to:

- Generate a synthetic image representing a simplified radio sky.
- Transform the image into the Fourier domain.
- Simulate incomplete Fourier measurements and add noise.
- Implement a zero-filled inverse Fourier transform as a baseline reconstruction method.
- Implement FISTA with an \(L_1\) sparsity regularisation term.
- Implement a Plug-and-Play reconstruction method using an image denoiser.
- Evaluate the methods using quantitative metrics and visual comparisons.
- Investigate the effects of sampling rate, noise level, and iteration count.

## 4. Mathematical Foundations

### 4.1 Representing the Sky Image

The synthetic sky is represented as a two-dimensional matrix:

$$
\mathbf{x}\in\mathbb{R}^{N\times N}
$$

where:

- $\mathbf{x}$ represents the complete image.
- $\mathbb{R}$ denotes the set of real numbers.
- $\mathbb{E}$ Belongs to/ Is an element of.
- $N$ is the number of rows and columns in the square image.

For this experiment, the image size is $64 \times 64$. Therefore,

$$
\mathbf{x}\in\mathbb{R}^{64\times64}
$$

The image contains $\(64\times64=4096\)$ pixel values.

The synthetic sky image is represented as a matrix:

$$
\mathbf{x}\in\mathbb{R}^{64\times64}
$$

More explicitly, the image matrix has the form:

$$
\mathbf{x}=
\begin{bmatrix}
x_{11} & x_{12} & \cdots & x_{1,64}\\
x_{21} & x_{22} & \cdots & x_{2,64}\\
\vdots & \vdots & \ddots & \vdots\\
x_{64,1} & x_{64,2} & \cdots & x_{64,64}
\end{bmatrix}
$$

The brightness at an individual pixel is represented by:

$$
x_{ij}
$$

Each $x_{ij}$ represents the brightness of a pixel at row $i$ and column $j$. The image contains $64\times64=4096$ pixel values.

where \(i\) is the row index and \(j\) is the column index.

For example, $x_{12}$ represents the brightness of the pixel at row 1, column 2 using mathematical indexing.

The synthetic image begins with a collection of point sources. Each source has a position and a brightness. The point sources are then smoothed using a Gaussian filter to create a simplified sky image.

### Point Sources

A point source is an idealised source of emission represented by a single location in an image. In this project, each point source is defined by its pixel coordinates and brightness.

The collection of $K$ point sources is represented as

$$
\mathcal{S}=\{(i_k,j_k,a_k)\}_{k=1}^{K}
$$

where:

- $K$ is the total number of point sources.
- $i_k$ is the row coordinate of source $k$.
- $j_k$ is the column coordinate of source $k$.
- $a_k$ is the brightness assigned to source $k$.

For this experiment, $K=8$. The sources are placed at predefined locations with different brightness values to create a sparse synthetic sky.

The initial sky image is constructed using

$$
x_{ij}=\sum_{k=1}^{K}a_k\delta_{i,i_k}\delta_{j,j_k}
$$

where $\delta$ is the Kronecker delta, which ensures that each source contributes brightness only at its assigned pixel location.

The sky begins as a collection of point sources. Each source is placed at a specific pixel location and assigned a brightness value.

For example,

$$
I(12,15)=1.0
$$

means that the pixel at row 12 and column 15 has brightness $\(1.0\)$.

Similarly,

$$
I(20,44)=0.8
$$

means that the pixel at row 20 and column 44 has brightness $\(0.8\)$.

### Mathematical Representation

Mathematically, the sky can be written as a sum of discrete point sources:

$$
I(x,y)=\sum_{k=1}^{8}a_k\,\delta(x-x_k,y-y_k)
$$

where:

- $a_k$ is the brightness of the $k$-th source.
- $(x_k, y_k)$ is the location of the $k$-th source.
- $\delta$ is the two-dimensional discrete delta (impulse) function.

### Example: A Single Point Source

For a single source located at $\((12,15)\)$ with brightness $\(1.0\)$:

$$
I(x,y)=1.0\,\delta(x-12,y-15)
$$

The minus signs do not indicate subtraction of brightness. They specify the location at which the delta function is centred.

The source is located where the arguments of the delta function are zero:

$$
x-12=0 \quad\Rightarrow\quad x=12
$$

and

$$
y-15=0 \quad\Rightarrow\quad y=15
$$

Thus,

$$
\delta(x-12,y-15)
$$

represents a point source at pixel $\((12,15)\)$.

### Two Dimensions

In this project, we use two-dimensional coordinates $(x,y)$ to identify pixel locations.

A point source at row 12, column 15 is represented mathematically as:

```math
\delta(x - 12, y - 15)
```

This function is non-zero only when:

```math
x = 12
```

and

```math
y = 15
```

Therefore, it represents a single bright pixel located at $(12,15)$.

### Complete Synthetic Sky

The complete synthetic sky consists of eight point sources:

$$
\begin{aligned}
I(x,y)={}&1.0\,\delta(x-12,y-15)\\
&+0.8\,\delta(x-20,y-44)\\
&+0.7\,\delta(x-36,y-18)\\
&+0.9\,\delta(x-47,y-48)\\
&+0.6\,\delta(x-29,y-32)\\
&+0.55\,\delta(x-51,y-12)\\
&+0.65\,\delta(x-14,y-51)\\
&+0.75\,\delta(x-41,y-35).
\end{aligned}
$$

Each delta function places a source at its specified pixel location, while its coefficient determines the source's brightness.

Our objective is to estimate $\mathbf{x}$ from incomplete and noisy Fourier measurements.

Therefore, the general measurement model is:

\mathbf{y} = \mathbf{M} \odot \mathcal{F}(\mathbf{x}) + \mathbf{M} \odot \mathbf{n}

where:

| Symbol | Meaning |
|---|---|
| $\mathbf{x}$ | Original sky image |
| $\mathcal{F}$ | Two-dimensional Fourier transform |
| $\mathbf{M}$ | Fourier sampling mask |
| $\odot$ | Element-wise multiplication |
| $\mathbf{n}$ | Simulated complex noise |
| $\mathbf{y}$ | Incomplete, noisy Fourier measurements |

This is the central equation behind the simulation.

The rest of the project is about understanding this equation and finding a good estimate of $\mathbf{x}$ from $\mathbf{y}$.

### 4.2 The Fourier Transform

The Fourier transform expresses an image in terms of spatial frequencies. These frequencies describe how image brightness varies across space.

The two-dimensional discrete Fourier transform (DFT) is defined here using an orthonormal normalisation convention:

$$
X_{uv}=
\frac{1}{N}
\sum_{i=0}^{N-1}
\sum_{j=0}^{N-1}
x_{ij}
\exp\left[
-\frac{2\pi\mathrm{i}}{N}(ui+vj)
\right]
$$

where:

- \(x_{ij}\) is the pixel brightness in the original image.
- \(X_{uv}\) is the Fourier coefficient at frequency coordinates \((u,v)\).
- \(N\) is the image dimension.
- \(\mathrm{i}=\sqrt{-1}\) is the imaginary unit.
- \(u\) and \(v\) index the spatial frequencies.

The Fourier coefficients are generally complex-valued. Each coefficient contains magnitude and phase information.

In Python, this transformation is implemented using:

```python
def fft2(image):
    return np.fft.fft2(image, norm="ortho")
```

The inverse Fourier transform converts the frequency-domain representation back into an image:

$$
x_{ij}=
\frac{1}{N}
\sum_{u=0}^{N-1}
\sum_{v=0}^{N-1}
X_{uv}
\exp\left[
\frac{2\pi\mathrm{i}}{N}(ui+vj)
\right]
$$

When all Fourier coefficients are available, the inverse transform can recover the original image, up to numerical precision. When measurements are missing, the problem becomes more difficult.

### 4.3 Incomplete Fourier Measurements

In this project, not every Fourier coefficient is observed. A binary sampling mask is used to indicate which measurements are available:

$$
M_{uv}\in\{0,1\}
$$

where:

$$
M_{uv}=
\begin{cases}
1,&\text{if the measurement is available},\\
0,&\text{if the measurement is missing}.
\end{cases}
$$

The incomplete measurement process is modelled as:

$$
y_{uv}=M_{uv}(X_{uv}+\sigma n_{uv})
$$

where:

- \(y_{uv}\) is the observed Fourier measurement.
- \(X_{uv}\) is the true Fourier coefficient.
- \(M_{uv}\) is the sampling mask.
- \(\sigma\) controls the noise amplitude.
- \(n_{uv}\) is a complex-valued noise sample.

The complete measurement model can also be written as:

$$
\mathbf{y}
=
\mathbf{M}\odot
\left(\mathcal{F}(\mathbf{x})+\sigma\mathbf{n}\right)
$$

Here, \(\mathcal{F}\) denotes the two-dimensional Fourier transform and \(\odot\) denotes element-wise multiplication.

A sampling fraction of approximately \(30\%\) is used as the initial target. The actual fraction may differ because the mask is adjusted to maintain conjugate symmetry for real-valued images.

This random sampling strategy is a simplified educational model. It does not reproduce the baseline geometry, visibility sampling, or other instrumental effects of a real radio interferometer.

### 4.4 Zero-Filled Inverse Fourier Reconstruction

The first reconstruction method is the zero-filled inverse Fourier transform.

Missing Fourier coefficients are treated as zero, and the inverse Fourier transform is applied:

$$
\mathbf{x}_{\mathrm{raw}}
=
\operatorname{Re}
\left\{
\mathcal{F}^{-1}(\mathbf{M}\odot\mathbf{y})
\right\}
$$

The real part is retained because the target image is real-valued.

A non-negativity constraint is then applied:

$$
\hat{x}_{ij}=\max(0,x_{\mathrm{raw},ij})
$$

where \(\hat{\mathbf{x}}\) is the reconstructed image.

This method provides a simple baseline, but missing Fourier measurements can produce blurring and artefacts. The non-negativity operation is a basic constraint rather than a complete physical model of radio imaging.

### 4.5 FISTA with \(L_1\) Sparsity

The Fast Iterative Shrinkage-Thresholding Algorithm (FISTA) is an optimisation method that can be used to reconstruct an image from incomplete measurements.

Define the forward measurement operator as:

$$
\mathcal{A}(\mathbf{x})
=
\mathbf{M}\odot\mathcal{F}(\mathbf{x})
$$

A sparse reconstruction can be formulated as:

$$
\min_{\mathbf{x}\geq0}
\frac{1}{2}
\left\|
\mathcal{A}(\mathbf{x})-\mathbf{y}
\right\|_2^2
+
\lambda\|\mathbf{x}\|_1
$$

where:

- The first term measures disagreement between predicted and observed measurements.
- The \(L_1\) norm encourages sparsity in the reconstructed image.
- \(\lambda\) controls the trade-off between data fidelity and sparsity.
- The non-negativity constraint requires the reconstructed brightness values to be non-negative.

The \(L_1\) norm is defined as:

$$
\|\mathbf{x}\|_1
=
\sum_{i,j}|x_{ij}|
$$

FISTA alternates gradient-based updates with a thresholding operation and uses momentum to accelerate convergence.

For the standard convex objective, FISTA has an \(O(1/k^2)\) convergence rate in objective value under the usual assumptions, where \(k\) is the iteration count. This guarantee depends on the optimisation formulation and does not automatically apply to every modified implementation.

### 4.6 Plug-and-Play Reconstruction

Plug-and-Play (PnP) reconstruction combines a measurement-consistency update with an image denoiser.

A simplified measurement-consistency step is:

$$
\mathbf{z}^{(k+1)}
=
\mathbf{x}^{(k)}
-
\eta\mathcal{A}^{*}
\left(
\mathcal{A}(\mathbf{x}^{(k)})-\mathbf{y}
\right)
$$

The denoising step is:

$$
\mathbf{x}^{(k+1)}
=
D_{\sigma_d}
\left(
\mathbf{z}^{(k+1)}
\right)
$$

where:

- \(k\) is the iteration index.
- \(\eta\) is the step size.
- \(\mathcal{A}^{*}\) is the adjoint of the measurement operator.
- \(D_{\sigma_d}\) is a denoising operator.
- \(\sigma_d\) controls the denoising strength.

The denoiser introduces an image prior into the reconstruction process. For the initial experiment, a Gaussian filter can be used as a simple denoiser. This is not a trained neural network.

PnP methods do not automatically inherit FISTA's convergence guarantees. Their behaviour depends on the measurement update, denoiser, step size, and other assumptions.

## 5. Reconstruction Methods

The project compares three approaches:

| Method | Description | Purpose |
|---|---|---|
| Zero-filled inverse FFT | Applies the inverse Fourier transform after filling missing measurements with zeros | Baseline |
| FISTA with \(L_1\) regularisation | Optimises data fidelity and image sparsity | Optimisation-based reconstruction |
| Plug-and-Play | Alternates measurement-consistency updates with denoising | Denoiser-based reconstruction |

The methods will be evaluated using the same synthetic sky and measurement data for each experiment. This helps make comparisons fair and reproducible.

## 6. Evaluation Metrics

### 6.1 Relative Reconstruction Error

The relative \(L_2\) reconstruction error compares the reconstructed image with the ground-truth image:

$$
E_{\mathrm{rel}}
=
\frac{
\|\hat{\mathbf{x}}-\mathbf{x}\|_2
}{
\|\mathbf{x}\|_2
}
$$

A smaller value indicates that the reconstructed image is closer to the ground truth in relative \(L_2\) error.

### 6.2 Mean Squared Error

The mean squared error (MSE) measures the average squared difference between corresponding pixels:

$$
\mathrm{MSE}
=
\frac{1}{N^2}
\sum_{i=0}^{N-1}
\sum_{j=0}^{N-1}
(\hat{x}_{ij}-x_{ij})^2
$$

A lower MSE indicates smaller average squared pixel errors.

### 6.3 Peak Signal-to-Noise Ratio

The peak signal-to-noise ratio (PSNR) is derived from MSE:

$$
\mathrm{PSNR}
=
10\log_{10}
\left(
\frac{L^2}{\mathrm{MSE}}
\right)
$$

where \(L\) is the maximum possible pixel value. For images normalised to the range \([0,1]\), \(L=1\).

A higher PSNR generally indicates lower pixel-wise reconstruction error. PSNR should be interpreted alongside visual inspection and other metrics.

### 6.4 Measurement Residual

The data residual measures disagreement between the reconstructed image and the available measurements:

$$
R_{\mathrm{data}}
=
\|\mathcal{A}(\hat{\mathbf{x}})-\mathbf{y}\|_2
$$

A smaller residual indicates better agreement with the observed measurements, although the smallest residual does not necessarily correspond to the most accurate image when measurements are noisy.

### 6.5 Convergence Behaviour

The reconstruction error, objective value where applicable, and measurement residual can be recorded over iterations.

These curves will help assess whether an algorithm stabilises and how quickly its reconstruction quality changes.

## 7. Experimental Design

The initial experiment uses the following settings:

| Parameter | Initial setting |
|---|---|
| Image dimensions | \(64\times64\) pixels |
| Target sampling fraction | \(30\%\) |
| Fourier noise scale | \(\sigma=0.01\) |
| Random seed | \(7\) |
| Initial reconstruction method | Zero-filled inverse FFT |

After the baseline has been tested, the experiment can be extended by changing one parameter at a time.

Suggested experiments include:

1. **Sampling fraction:** compare lower and higher proportions of observed Fourier coefficients.
2. **Noise level:** investigate the effect of increasing measurement noise.
3. **Regularisation strength:** assess how the choice of \(\lambda\) affects FISTA.
4. **Denoising strength:** assess how \(\sigma_d\) affects PnP.
5. **Iteration count:** compare reconstruction quality and stability over time.

For a fair comparison, use fixed random seeds and the same ground-truth image, mask, and measurements when comparing reconstruction algorithms. Report any parameter tuning and avoid selecting settings solely because they perform well on one test image.

## 8. Project Structure

The intended project structure is:

```text
radio-sky-reconstruction/
├── .venv/
├── src/
│   └── reconstruct.py
├── results/
│   └── first_reconstruction.png
├── requirements.txt
└── README.md
```

- `src/reconstruct.py`: generates the synthetic sky, simulates measurements, performs the baseline reconstruction, and saves the initial visualisation.
- `results/`: stores generated images and, in future, evaluation plots and numerical results.
- `requirements.txt`: lists the Python dependencies.
- `README.md`: documents the research question, mathematical model, methods, and experiments.

## 9. Requirements

The project uses Python and the following libraries:

- NumPy
- SciPy
- Matplotlib

Install the dependencies in an activated virtual environment:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
numpy
scipy
matplotlib
```

## 10. Running the Project

From the project root directory, activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the initial reconstruction:

```bash
python src/reconstruct.py
```

The program prints the image size, actual sampling fraction, and relative reconstruction error. It also displays a visual comparison of:

1. The ground-truth synthetic sky.
2. The Fourier sampling mask.
3. The zero-filled reconstruction.

The generated image is saved to:

```text
results/first_reconstruction.png
```

## 11. Current Scope and Limitations

This project is a simplified computational imaging experiment. Its limitations include:

- The sky image is synthetically generated rather than obtained from real astronomical observations.
- The sampling mask is randomly generated and does not represent realistic interferometer baseline coverage.
- The noise model is simplified and does not capture all sources of instrumental or observational noise.
- The initial reconstruction method is deliberately simple.
- A Gaussian denoiser is only a starting point for PnP and does not represent a learned image prior.
- Results on a single synthetic image cannot establish that a method will generalise to real radio astronomy data.
- PnP convergence must be investigated rather than assumed.

These limitations will be documented when reporting results.

## 12. Expected Outcomes

The project aims to produce:

- A reproducible synthetic reconstruction experiment.
- A baseline reconstruction against which more advanced methods can be compared.
- Implementations of FISTA and Plug-and-Play reconstruction.
- Quantitative comparisons using reconstruction error, MSE, PSNR, and measurement residuals.
- Plots showing the effect of sampling, noise, and iteration count.
- A discussion of the trade-offs between data fidelity, sparsity, denoising, and convergence behaviour.

The results will be used to assess the strengths and weaknesses of the tested methods under the specific experimental conditions, rather than to claim that one method is universally superior.

## 13. Research Motivation

Recovering images from incomplete measurements is a central challenge in computational imaging. The problem connects Fourier analysis, inverse problems, optimisation, regularisation, and prior-based reconstruction.

This project provides a practical foundation for exploring those concepts in a controlled setting. It also creates an opportunity to investigate how reconstruction accuracy and algorithmic stability change when information is missing or measurements are noisy.

## 14. Further Reading

The following foundational works provide context for the methods used in this project:

- Beck, A. and Teboulle, M. (2009). *A Fast Iterative Shrinkage-Thresholding Algorithm for Linear Inverse Problems.* SIAM Journal on Imaging Sciences, 2(1), 183–202.
- Venkatakrishnan, S. V., Bouman, C. A. and Wohlberg, B. (2013). *Plug-and-Play Priors for Model Based Reconstruction.* IEEE Global Conference on Signal and Information Processing.
- Fessler, J. A. (2010). *Model-Based Image Reconstruction for MRI.* IEEE Signal Processing Magazine, 27(4), 81–89.

These references provide background on accelerated proximal optimisation, Plug-and-Play priors, and model-based image reconstruction. They do not imply that the present simplified experiment reproduces the full methods or assumptions in those works.

---

**Project status:** Initial synthetic sky generation, Fourier sampling, and zero-filled inverse FFT reconstruction are the first implementation stage. FISTA, Plug-and-Play, and systematic evaluation are planned extensions.
