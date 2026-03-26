---
title: "One Marking, One Failure: An Attempt at Asymmetric Balancing Dilation"
date: 2026-03-25
author: "Zinan Huang"
tags: [population-protocols, CRN, one-marking, balancing-dilation, research-notes]
math: true
---

*We tried a new way to do balancing dilation. It didn't work. Here's why.*

<!--more-->

## What Are We Trying to Do?

A **population protocol** (PP) is a model of distributed computation. A collection of agents interact in pairs, updating their states. Formally, we have $n$ species $x\_1, \ldots, x\_n$ evolving by:

$$\dot{x}\_i = P\_i(x\_1, \ldots, x\_n), \quad i = 1, \ldots, n,$$

where each $P\_i$ is degree-2 homogeneous with $\sum\_i P\_i = 0$. The system lives on the simplex $\Delta = \\{(x\_1, \ldots, x\_n) : x\_i \geq 0,\; \sum x\_i = 1\\}$.

A **chemical reaction network** (CRN) implements a PP if bimolecular reactions among CRN species reproduce the PP dynamics via mass-action kinetics. The CRN species form a *variable system*: each species tracks some function of the original PP concentrations.

### The Four Desirable Properties

A variable system $\\{z\_\alpha\\}$ is:

1. **(P1) PP-implementable** if every $\dot{z}\_\alpha$ decomposes into terms $\pm k \cdot z\_\beta z\_\gamma$ (bimolecular reactions).
2. **(P2) Formally conservative** if $\sum\_\alpha \dot{z}\_\alpha = 0$ as a polynomial identity.
3. **(P3) One-marking** if the target $x\_1^\*$ can be read from a single species: $z\_1 \to c \cdot x\_1^\*$. Ideally $c = 1$.
4. **(P4) Non-autocatalytic (NAP)** if no reaction has the form $A + B \to A + A$.

Achieving all four simultaneously is hard. Our approach uses *balancing dilation*.

## Balancing Dilation

Given the PP ODE $\dot{x}\_i = P\_i(\mathbf{x})$ with $\deg P\_i = 2$, we introduce a fresh variable $r$ and replace:

$$\dot{x}\_i \;\longmapsto\; r^k \cdot P\_i(\mathbf{x})$$

for some $k \geq 1$. This slows the dynamics by $r^k$ but preserves the fixed point (since $r^\* > 0$). The higher degree gives more room for bimolecular decompositions.

### The $\frac{1}{2}$-Trick

The simplest version uses $k = 1$ and the variable system from $\frac{1}{2}(S + S^2)$, where $S = r + x\_1 + \cdots + x\_n$.

For a single-species PP ($n = 1$), $S = r + x$, giving 5 variables:

| # | Name | Definition | Source |
|---|------|-----------|--------|
| 1 | $a\_r$ | $\frac{1}{2}r$ | $\frac{1}{2}S$ |
| 2 | $a\_x$ | $\frac{1}{2}x$ | $\frac{1}{2}S$ |
| 3 | $b\_{rr}$ | $\frac{1}{2}r^2$ | $\frac{1}{2}S^2$ |
| 4 | $b\_{rx}$ | $rx$ | $\frac{1}{2}S^2$ |
| 5 | $b\_{xx}$ | $\frac{1}{2}x^2$ | $\frac{1}{2}S^2$ |

Here $r = 1 - x$ (an algebraic identity). Total mass: $\frac{1}{2}S + \frac{1}{2}S^2 = 1$ on the simplex.

**Why this works (G1 — PP-implementable closure):**

- Degree-1 variables' derivatives (degree 3) factor as (deg-1) × (deg-2) products.
- Degree-2 variables' derivatives (degree 4) factor as (deg-2) × (deg-2) products.
- Formal conservation is automatic: $\frac{d}{dt}[\frac{1}{2}S + \frac{1}{2}S^2] = \frac{S'}{2}(1 + 2S) = 0$.

Verified for the CF'24 running example: an LP finds 10 valid bimolecular reactions.

**The two defects:**

- **B1:** The marking variable $a\_x = \frac{1}{2}x$ tracks *half* the target. Readout: $x^\* = 2a\_x^\*$.
- **B2:** The uniform $\frac{1}{2}$ scaling is structurally necessary. Without it, $S + S^2 = 2$ on the simplex.

Not fatal — but inelegant. Can we do better?

## The New Idea: Method of Unknowns

### Motivation

The $\frac{1}{2}$-trick scales *everything* by $\frac{1}{2}$, including the marking variable. What if we break the symmetry?

**Proposal:** Keep $x\_1$ unscaled (direct readout) and scale everything else by a small $\lambda > 0$. Introduce an independent variable $r$ to absorb conservation.

### The Philosophical Shift

In the $\frac{1}{2}$-trick, $r = 1 - \sum x\_i$ is a *derived quantity*: algebraically determined by the PP species. Its derivative $\dot{r} = -\sum \dot{x}\_i$ follows by differentiation.

In the new construction, $r$ is an **independent unknown** — a CRN species in its own right. We don't define what $r$ "is." We only require:

1. **Conservation:** $r + \sum\_{\alpha \neq r} z\_\alpha = 1$.
2. **Dilation:** $\dot{x}\_i = r \cdot P\_i(x\_1, \ldots, x\_n)$.
3. **Absorber:** $\dot{r} = -\sum\_{\alpha \neq r} \dot{z}\_\alpha$.

Condition 3 follows from differentiating Condition 1. This is the **method of unknowns**: we don't prescribe $r$'s identity, only the constraints it must satisfy.

### The Variable System

For small $\lambda > 0$:

- $x\_1$ — marking, unscaled (direct readout)
- $\lambda x\_i$, $i = 2, \ldots, n$ — other species, scaled
- $\lambda r x\_i$, $i = 1, \ldots, n$ — degree-2 cross terms
- $\lambda r x\_i x\_j$, $i \leq j$ — degree-3 cross terms
- $\lambda r^2$ — degree-2 pure-$r$
- $r$ — conservation absorber

Structurally the same monomial family as $S + S^2$, just with asymmetric coefficients.

## Why It Fails: The Circularity of $\dot{r}$

### The Chain-Rule Trap

Consider $z = \lambda r x\_1$. For $z$ to faithfully represent the product of species $r$ and $x\_1$, the chain rule requires:

$$\dot{z} = \lambda(\dot{r} \cdot x\_1 + r \cdot \dot{x}\_1).$$

But $\dot{r}$ is the conservation absorber: $\dot{r} = -\sum\_{\alpha \neq r} \dot{z}\_\alpha$. And $\dot{z}$ is one of those terms. So $\dot{r}$ depends on $\dot{z}$, and $\dot{z}$ depends on $\dot{r}$. **Circular.**

### Resolving the Circularity (and Hitting a Wall)

We can solve for $\dot{r}$ explicitly. For $n = 1$ with variables $\\{x, \lambda rx, \lambda r^2, r\\}$:

$$\dot{r} = -[\dot{x} + \lambda(\dot{r} \cdot x + r \cdot \dot{x}) + 2\lambda r \cdot \dot{r}]$$

Collecting $\dot{r}$ terms:

$$\dot{r}(1 + \lambda x + 2\lambda r) = -\dot{x}(1 + \lambda r).$$

Substituting $\dot{x} = rP$ (after $r$-dilation):

$$\boxed{\dot{r} = \frac{-rP(1 + \lambda r)}{1 + \lambda x + 2\lambda r}.}$$

This is a **rational function** of $r$ and $x$.

### Why This Is Fatal

Mass-action CRNs produce **polynomial** ODEs. Each reaction $A + B \to C + D$ at rate $k$ contributes $\pm k[A][B]$ — always a polynomial. The resulting ODE for each species is at most degree 2 in bimolecular systems.

The denominator $1 + \lambda x + 2\lambda r$ depends on species concentrations and does not simplify to a constant (even on the simplex). No set of bimolecular reactions can produce a rational-function ODE.

### Why the $\frac{1}{2}$-Trick Avoids This

In the $\frac{1}{2}$-trick, $r = 1 - x$ is an algebraic identity. So $\dot{r} = -\dot{x}$ — a polynomial. No circularity, because $r$ is not independent.

The price: uniform $\frac{1}{2}$ scaling (B1 and B2). The method of unknowns tried to eliminate this price by making $r$ independent. But independence creates circularity, and circularity creates rational functions.

## The Structural Lesson

The failure isn't accidental. It reflects a fundamental tension:

1. **Direct readout** requires asymmetric scaling ($x\_1$ unscaled, rest scaled by $\lambda$).
2. **Formal conservation** requires an absorber ($\dot{r}$ cancels everything else).
3. **Chain-rule consistency** requires compound variables ($\lambda rx$, $\lambda r^2$) to obey the product rule.
4. **Combining (2) and (3):** $\dot{r}$ appears on both sides of the conservation equation. Solving yields a rational function.

The $\frac{1}{2}$-trick resolves this by making $r$ *dependent* (eliminating circularity but forcing uniform scaling). We tried to have both independent $r$ and chain-rule consistency. These two goals are **incompatible**.

## What Remains

| Construction | One marking | Formal cons. | Simplex | Issue |
|---|---|---|---|---|
| Self-product ($z\_{ij} = x\_i x\_j$) | No (two) | Yes | Yes | $O(n^2)$ markings |
| $\frac{1}{2}$-trick | Yes | Yes | Yes | Tracks $\frac{1}{2}x^\*$ |
| $\sqrt{\cdot}$ method | Yes | Yes | No | $\sqrt{x} > x$ for $x < 1$ |
| **Method of unknowns** | Yes | Yes | Yes | **Rational $\dot{r}$ (fatal)** |

Every approach eliminates some defects but introduces new ones. The $\frac{1}{2}$-trick remains the most viable. Whether direct readout ($c = 1$) with polynomial dynamics is achievable remains open.

---

*This is joint work with [Xiang Huang](https://xianghuang.org). The method of unknowns was his idea; the verification and failure analysis are mine. Filed under "negative results worth documenting."*
