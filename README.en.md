# Adaptive Weighted Random Roll Call

[GitHub](https://github.com/Epslion404/Adaptive-weight-random-roll-call)

#### Introduction

A more equitable random roll call system designed for short-term fairness.  
**This project uses the Lucky Block MOD from Minecraft as an icon. Please notify me immediately if this cannot be used.**

#### Software Architecture

Developed with Python 3.8.

#### Installation Guide

1. Install Python 3.8.
2. Run the `install modules.bat` file to install the required libraries.
3. Follow the instructions in `main.py` to input the list of names and delimiter.
4. Execute the `main.py` file to ensure the program runs correctly.
5. Use the command `pyinstaller -F -w -i favicon.ico main.py` or run `pack to exe.bat` to package the program into an executable file.

#### Usage Instructions

You can either run the `main.py` file directly or use the packaged executable.

#### TO DO

- [x] Initialize the repository
- [x] Make the old code more understandable (80%)
- [ ] Fix bugs (e.g., child processes fail to exit after the main process ends)
- [x] Encrypt the configuration file
- [x] Adjust based on uncalled times
- [x] Record data by category
- [x] Store data in JSON format
- [x] Prevent duplicate starts
- [x] Minimize to tray icon
- [ ] Customize the ratio of frequency adjustment to uncalled times adjustment

#### Principles

Random functions can produce uneven results in the short term, leading to unrealistic assumptions and biases about randomness in roll calls. To address this while maintaining randomness, we introduce a negative feedback mechanism using weighted random functions.

The initial approach involves using the Reciprocal Frequency Adjustment method (RFA). This method adjusts the weights based on the reciprocal of each individual's selection frequency. To handle cases where the frequency is zero, we add 1 to everyone's frequency during calculations:
$$
w = \frac{1}{f_n + 1}
$$
Controlling the intensity of feedback adjustment is also crucial. By introducing a negative feedback strength $\Psi$, the weight can be expressed as:
$$
w_n = \frac{\hat f_n}{\Sigma f}
$$
where $\hat f_n$ represents the frequency with feedback included. If $\bar{f}$ denotes the overall average frequency, then $\hat f_n$ is defined as:
$$
\hat f_n=\begin{cases}
\ \frac{\Psi}{f_n + 1}, & f_n < \bar{f} \\
\ \frac{1}{\Psi(f_n + 1)}, & f_n > \bar{f} \\
\ \frac{1}{f_n + 1}, & f_n = \bar{f}
\end{cases}
$$  
The sum $\Sigma f$ is:
$$
\Sigma f = \sum_{i=0}^{m} \begin{cases}
\ \frac{\Psi}{f_i + 1}, & f_i < \bar{f} \\
\ \frac{1}{\Psi(f_i + 1)}, & f_i > \bar{f} \\
\ \frac{1}{f_i + 1}, & f_i = \bar{f}
\end{cases}
$$

However, as the software is used over time, it is often observed that a student might not be selected for an extended period, only to be frequently chosen in a short span after a long period, leading their individual frequency to quickly align with the average. Therefore, in addition to macro adjustments, micro adjustments are necessary. To address this, we record the number of times each student has been skipped since their last selection ($\mu$) and adjust accordingly (NLT). In this context, the weight is expressed as:
$$
w_n = r_f \cdot \frac{\hat f_n}{\Sigma f} + r_\mu \cdot \frac{\hat \mu_n}{\Sigma \mu}
$$
where $r_f$ and $r_\mu$ represent the proportions of RFA and NLT adjustments, respectively. $\hat \mu_n$ represents the number of times skipped since the last call with feedback. If $\bar{\mu}$ denotes the overall average number of times skipped, then $\hat \mu_n$ is defined as:
$$
\hat \mu_n=\begin{cases}
\ \frac{\Psi \mu_n}{\Sigma \mu}, & \mu_n < \bar{\mu} \\
\ \frac{\mu_n}{\Psi \Sigma \mu}, & \mu_n > \bar{\mu} \\
\ \frac{\mu}{\Sigma \mu}, & \mu_n = \bar{\mu}
\end{cases}
$$
The sum $\Sigma \mu$ is:
$$
\Sigma \mu = \sum_{i=0}^{m} \begin{cases}
\ \Psi \mu_i, & \mu_i < \bar{\mu} \\
\ \frac{\mu_i}{\Psi}, & \mu_i > \bar{\mu} \\
\ \mu_i, & \mu_i = \bar{\mu}
\end{cases}
$$

#### Contributions

As of now, there are no additional contributors besides myself φ(゜▽゜*)♪