# Adaptive Weighted Random Roll Call

[GitHub](https://github.com/Epslion404/Adaptive-weight-random-roll-call)  
**Note: This project uses the Lucky Block MOD from Minecraft as the icon. If there are any usage issues, please notify me immediately.**

## Introduction

A short-term fairer random roll call system designed to improve equity in selection processes. By introducing adaptive weighting mechanisms, it reduces short-term unevenness in random results and minimizes potential biases.

## Software Architecture

Built with Python 3.8.

## Installation Guide

1. Install Python 3.8 or later
2. Run `install modules.bat` to install required dependencies
3. Configure the name list and delimiter in `main.py` as instructed
4. Test run `main.py` to verify proper execution
5. Package into executable using: `pyinstaller -F -w -i favicon.ico main.py` 
   or simply run `pack to exe.bat`

## Usage

Run `main.py` directly or launch the packaged executable.

## Development Progress

- [x] Initialize repository
- [x] Refactor legacy code (80% comprehensibility)
- [x] Fix bugs (child process termination after main process ends)
- [x] Encrypt configuration files
- [x] Implement adjustment based on uncalled times
- [x] Category-based data recording
- [x] JSON format data storage
- [x] Prevent duplicate launches
- [x] Minimize to system tray
- [x] Customizable ratio between frequency adjustment and uncalled times adjustment
- [x] Custom adjustment ratios
- [ ] Visualization of adjustment effects
- [ ] Custom encryption keys

## Algorithm Principles

Conventional random functions often produce uneven short-term results, leading to unrealistic assumptions about "randomness". Our solution incorporates negative feedback through weighted random functions.

### Primary Method: Reciprocal Frequency Adjustment (RFA)
Uses inverse frequency as weighting factor, with +1 adjustment for zero-frequency cases:

$$
w = \frac{1}{f_n + 1}
$$

With feedback strength $\Psi$, the weight becomes:

$$
w_n = \frac{\hat f_n}{\Sigma f}
$$

Where $\hat f_n$ represents frequency with feedback:

$$
\hat f_n = \begin{cases}
\frac{\Psi}{f_n + 1}, & f_n < \bar{f} \\
\frac{1}{\Psi(f_n + 1)}, & f_n > \bar{f} \\
\frac{1}{f_n + 1}, & f_n = \bar{f}
\end{cases}
$$

And $\Sigma f$ denotes:

$$
\Sigma f = \sum_{i=0}^{m} \begin{cases}
\frac{\Psi}{f_i + 1}, & f_i < \bar{f} \\
\frac{1}{\Psi(f_i + 1)}, & f_i > \bar{f} \\
\frac{1}{f_i + 1}, & f_i = \bar{f}
\end{cases}
$$

### Enhanced Method: Number of Times Since Last Call (NLT)
Addresses prolonged non-selection periods by tracking times since last call ($\mu$):

$$
w_n = r_f \cdot \frac{\hat f_n}{\Sigma f} + r_\mu \cdot \frac{\hat \mu_n}{\Sigma \mu}
$$

Where $r_f$ and $r_\mu$ represent RFA and NLT ratios respectively, and $\hat \mu_n$ incorporates feedback:

$$
\hat \mu_n = \begin{cases}
\frac{\Psi(\mu_n + 1)}{\Sigma \mu}, & \mu_n < \bar{\mu} \\
\frac{\mu_n + 1}{\Psi \Sigma \mu}, & \mu_n > \bar{\mu} \\
\frac{\mu + 1}{\Sigma \mu}, & \mu_n = \bar{\mu}
\end{cases}
$$

With $\Sigma \mu$ calculated as:

$$
\Sigma \mu = \sum_{i=0}^{m} \begin{cases}
\Psi(\mu_i + 1), & \mu_i < \bar{\mu} \\
\frac{\mu_i + 1}{\Psi}, & \mu_i > \bar{\mu} \\
\mu_i + 1, & \mu_i = \bar{\mu}
\end{cases}
$$

## Performance Comparison

### Legacy Version
**Without feedback** (console output shows variance):  
![img](img/自然随机%20重复%20100次.png)

**With feedback (Ψ=3)**:  
![img](img/反馈随机%20重复%20100次.png)

### Current Version
**Without feedback** (frequency variance: 0.846):  
![img](img/新版%20自然随机%2026次.png)

**With feedback (Ψ=2, $r_u = r_f = 0.5$)** (variance: 0.308):  
![img](img/新版%20反馈随机%2026次.png)

## Contributions

Currently maintained solely by myself φ(゜▽゜*)♪  
Contributions and suggestions are welcome!

---
*Note: This project is designed for educational environments where short-term fairness in random selection is desired. The algorithm ensures that while maintaining randomness, the selection distribution becomes more balanced over time.*
