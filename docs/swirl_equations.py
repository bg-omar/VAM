from __future__ import annotations
from docs.generate_equation_class import latex_to_python

class SwirlEquations:
    """Collection of LaTeX equations extracted from VAM tex files."""
    def __init__(self):
        pass

    def equation_1(self, as_latex: bool = True) -> str:
        """Return equation 1 as LaTeX or Python string."""
        eq = r"""\boxed{
                \frac{d\tau}{d\mathcal{N}} = \sqrt{1 - \frac{|\vec{v}_\theta|^2}{c^2}}, \quad |\vec{v}_\theta| = |\vec{\omega}| r
            }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_2(self, as_latex: bool = True) -> str:
        """Return equation 2 as LaTeX or Python string."""
        eq = r"""\boxed{
                \nabla S(t) = \frac{dS}{d\mathcal{N}} + \vec{\omega}(\tau) \cdot \hat{n}
            }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_3(self, as_latex: bool = True) -> str:
        """Return equation 3 as LaTeX or Python string."""
        eq = r"""\boxed{
                T_v = \oint \frac{ds}{v_\text{phase}}
            }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_4(self, as_latex: bool = True) -> str:
        """Return equation 4 as LaTeX or Python string."""
        eq = r"""\boxed{
                L = L_0 \sqrt{1 - \frac{v^2}{c^2}}.
            }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_5(self, as_latex: bool = True) -> str:
        """Return equation 5 as LaTeX or Python string."""
        eq = r"""\boxed{
                ds^2 = C_e^2 dT_v^2 - dr^2
            }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_6(self, as_latex: bool = True) -> str:
        """Return equation 6 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\mathcal{N}} = \sqrt{1 - \frac{|\vec{v}_\theta|^2}{c^2}}, \quad \text{where } |\vec{v}_\theta| = |\vec{\omega}| r"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_7(self, as_latex: bool = True) -> str:
        """Return equation 7 as LaTeX or Python string."""
        eq = r"""\delta T_v = \oint_{\text{before}} \frac{ds}{v_\text{phase}} - \oint_{\text{after}} \frac{ds}{v'_\text{phase}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_8(self, as_latex: bool = True) -> str:
        """Return equation 8 as LaTeX or Python string."""
        eq = r"""\mathcal{R}_{\text{swirl}} = \nabla \cdot (\vec{\omega} \times \vec{v})"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_9(self, as_latex: bool = True) -> str:
        """Return equation 9 as LaTeX or Python string."""
        eq = r"""\boxed{
            \frac{d\tau}{d\mathcal{N}} = \sqrt{1 - \frac{\Gamma^2}{4\pi^2 r^2 c^2}}
        }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_10(self, as_latex: bool = True) -> str:
        """Return equation 10 as LaTeX or Python string."""
        eq = r"""\frac{d^{2x^i}}{ds^2} = \partial^i \log n(x)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_11(self, as_latex: bool = True) -> str:
        """Return equation 11 as LaTeX or Python string."""
        eq = r"""G_{\mu\nu}^{\text{eff}} = \kappa \, T_{\mu\nu}^{\text{(vortex)}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_12(self, as_latex: bool = True) -> str:
        """Return equation 12 as LaTeX or Python string."""
        eq = r"""v_\varphi(r) = \frac{1}{r} \int_0^r \omega(r') \, r' \, dr'"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_13(self, as_latex: bool = True) -> str:
        """Return equation 13 as LaTeX or Python string."""
        eq = r"""\omega(r) = \omega_0 \cdot \frac{r}{r^2 + r_c^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_14(self, as_latex: bool = True) -> str:
        """Return equation 14 as LaTeX or Python string."""
        eq = r"""v_\varphi(r)
    = \omega_0 \left( 1 - \frac{r_c}{r} \arctan\left( \frac{r}{r_c} \right) \right)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_15(self, as_latex: bool = True) -> str:
        """Return equation 15 as LaTeX or Python string."""
        eq = r"""\boxed{
        v_\text{core}(r) = \frac{C_{\text{core}}}{\sqrt{1 + \left( \frac{r_c}{r} \right)^2 }}
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_16(self, as_latex: bool = True) -> str:
        """Return equation 16 as LaTeX or Python string."""
        eq = r"""\Omega(r) = \frac{v_\varphi(r)}{r}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_17(self, as_latex: bool = True) -> str:
        """Return equation 17 as LaTeX or Python string."""
        eq = r"""\Omega(r) = \Omega_0 \left( 1 - e^{-r/r_c} \right)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_18(self, as_latex: bool = True) -> str:
        """Return equation 18 as LaTeX or Python string."""
        eq = r"""\boxed{
    v_\text{tail}(r) = C_{\text{tail}} \left(1 - e^{-r/r_c} \right)
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_19(self, as_latex: bool = True) -> str:
        """Return equation 19 as LaTeX or Python string."""
        eq = r"""\boxed{
    v(r) = \frac{C_{\text{core}}}{\sqrt{1 + \left( \frac{r_c}{r} \right)^2}} + C_{\text{tail}} \left(1 - e^{-r/r_c} \right)
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_20(self, as_latex: bool = True) -> str:
        """Return equation 20 as LaTeX or Python string."""
        eq = r"""F^{\text{max}}_{\text{\ae}} = \alpha  \left(\frac{c^4}{4G}\right) \left(\frac{R_c}{L_p}\right)^{-2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_21(self, as_latex: bool = True) -> str:
        """Return equation 21 as LaTeX or Python string."""
        eq = r"""M_e = \frac{8\pi \rho_\text{\ae} r_c^3}{C_e}\, L_k"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_22(self, as_latex: bool = True) -> str:
        """Return equation 22 as LaTeX or Python string."""
        eq = r"""\hbar = \sqrt{\frac{2 M_e F^{\text{max}}_{\text{\ae}} r_c^3}{5 \lambda_c C_e}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_23(self, as_latex: bool = True) -> str:
        """Return equation 23 as LaTeX or Python string."""
        eq = r"""i \hbar \frac{\partial \psi}{\partial t} = -\frac{F^{\text{max}}_{\text{\ae}} r_c^3}{5 \lambda_c C_e}\nabla^2 \psi + V\psi"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_24(self, as_latex: bool = True) -> str:
        """Return equation 24 as LaTeX or Python string."""
        eq = r"""\rho_{\text{\ae}}^{\text{(fluid)}} \approx \SI{7e-7}{kg/m^3},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_25(self, as_latex: bool = True) -> str:
        """Return equation 25 as LaTeX or Python string."""
        eq = r"""\rho_{\text{\ae}}^{\text{(energy)}}(r \to 0) \sim \SI{3.89e18}{J/m^3},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_26(self, as_latex: bool = True) -> str:
        """Return equation 26 as LaTeX or Python string."""
        eq = r"""E_{\text{vortex}} = \frac{1}{2} \rho_{\text{\ae}}^{\text{(energy)}} \Omega^2 r_c^5
    \quad\Rightarrow\quad
    \rho_{\text{\ae}}^{\text{(energy)}} \sim \frac{2E}{\Omega^2 r_c^5},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_27(self, as_latex: bool = True) -> str:
        """Return equation 27 as LaTeX or Python string."""
        eq = r"""\rho_{\text{\ae}}^{\text{(energy)}}(r) =
    \rho_{\text{\ae}}^{\text{(fluid)}} +
    \left(\rho_{\text{core}} - \rho_{\text{\ae}}^{\text{(fluid)}}\right)
    e^{-r/r_*},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_28(self, as_latex: bool = True) -> str:
        """Return equation 28 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} = \sqrt{1 - \frac{v_{\phi}^2(r)}{c^2}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_29(self, as_latex: bool = True) -> str:
        """Return equation 29 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\bar{t}} = \frac{\omega_{\text{obs}}}{\omega_0}
    \quad \text{(Chronos vs. External Clock Time)}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_30(self, as_latex: bool = True) -> str:
        """Return equation 30 as LaTeX or Python string."""
        eq = r"""\fbox{
        \(
        \frac{d\tau}{d\bar{t}} = e^{-r/r_c}
        \)}
    \quad \text{where } \Omega(r) = \frac{C_e}{r_c} e^{-r/r_c}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_31(self, as_latex: bool = True) -> str:
        """Return equation 31 as LaTeX or Python string."""
        eq = r"""P + \frac{1}{2}\rho_\text{\ae} v^2 = \text{constant}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_32(self, as_latex: bool = True) -> str:
        """Return equation 32 as LaTeX or Python string."""
        eq = r"""v_{\phi}(r) = \frac{\Gamma}{2\pi r} = \frac{\kappa}{r}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_33(self, as_latex: bool = True) -> str:
        """Return equation 33 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} = \sqrt{1 - \frac{\kappa^2}{c^2 r^2}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_34(self, as_latex: bool = True) -> str:
        """Return equation 34 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} = \sqrt{1 - \frac{2GM}{rc^2}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_35(self, as_latex: bool = True) -> str:
        """Return equation 35 as LaTeX or Python string."""
        eq = r"""S \propto \int_V \|\vec{\omega}\|^2 \, dV,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_36(self, as_latex: bool = True) -> str:
        """Return equation 36 as LaTeX or Python string."""
        eq = r"""\Gamma = \oint \vec{v} \cdot d\vec{l} = n \cdot \kappa,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_37(self, as_latex: bool = True) -> str:
        """Return equation 37 as LaTeX or Python string."""
        eq = r"""H = \int \vec{v} \cdot \vec{\omega} \, dV,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_38(self, as_latex: bool = True) -> str:
        """Return equation 38 as LaTeX or Python string."""
        eq = r"""dS = \frac{\delta Q}{T},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_39(self, as_latex: bool = True) -> str:
        """Return equation 39 as LaTeX or Python string."""
        eq = r"""dS = \frac{\delta \Pi_\text{rot}}{\mathcal{T}_\omega},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_40(self, as_latex: bool = True) -> str:
        """Return equation 40 as LaTeX or Python string."""
        eq = r"""\nabla P = -\rho_\text{\ae} (\vec{v} \cdot \nabla) \vec{v},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_41(self, as_latex: bool = True) -> str:
        """Return equation 41 as LaTeX or Python string."""
        eq = r"""\frac{dS}{dt} = \int_V \frac{\nabla \cdot \vec{J}_\text{vortex}}{T_\omega} \, dV,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_42(self, as_latex: bool = True) -> str:
        """Return equation 42 as LaTeX or Python string."""
        eq = r"""\Delta V_\text{knot} = \alpha_\omega V_0 \Delta T_\omega,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_43(self, as_latex: bool = True) -> str:
        """Return equation 43 as LaTeX or Python string."""
        eq = r"""\alpha_\omega = \frac{1}{r_c} \frac{d r_k}{d T_\omega} \sim \frac{C_e^2}{r_c k_B T_\omega},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_44(self, as_latex: bool = True) -> str:
        """Return equation 44 as LaTeX or Python string."""
        eq = r"""\oint \frac{\delta Q}{T} \leq 0,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_45(self, as_latex: bool = True) -> str:
        """Return equation 45 as LaTeX or Python string."""
        eq = r"""\oint \frac{\vec{v} \cdot d\vec{\omega}}{\mathcal{T}_\omega} \leq 0,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_46(self, as_latex: bool = True) -> str:
        """Return equation 46 as LaTeX or Python string."""
        eq = r"""\eta = 1 - \frac{T_C}{T_H},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_47(self, as_latex: bool = True) -> str:
        """Return equation 47 as LaTeX or Python string."""
        eq = r"""\eta_\text{VAM} = 1 - \frac{\Omega_C^2}{\Omega_H^2},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_48(self, as_latex: bool = True) -> str:
        """Return equation 48 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\mathcal{N}} = \left(1 + \beta \Omega_k^2 \right)^{-1}
    \quad \text{(Chronos-Time slowdown due to internal vortex rotation)}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_49(self, as_latex: bool = True) -> str:
        """Return equation 49 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\mathcal{N}} \approx 1 - \beta \Omega_k^2 + \mathcal{O}(\Omega_k^4)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_50(self, as_latex: bool = True) -> str:
        """Return equation 50 as LaTeX or Python string."""
        eq = r"""\frac{t_\text{moving}}{t_\text{rest}} \approx 1 - \frac{v^2}{2c^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_51(self, as_latex: bool = True) -> str:
        """Return equation 51 as LaTeX or Python string."""
        eq = r"""E_\text{rot} = \frac{1}{2} I \Omega_k^2"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_52(self, as_latex: bool = True) -> str:
        """Return equation 52 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\mathcal{N}} = \left(1 + \beta E_\text{rot} \right)^{-1}
    = \left(1 + \frac{1}{2} \beta I \Omega_k^2 \right)^{-1}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_53(self, as_latex: bool = True) -> str:
        """Return equation 53 as LaTeX or Python string."""
        eq = r"""H = \int \vec{v} \cdot \vec{\omega} \, d^3x"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_54(self, as_latex: bool = True) -> str:
        """Return equation 54 as LaTeX or Python string."""
        eq = r"""\left( \frac{d\tau_{\text{GR}}}{dt} \right)^2 = -\left[ g_{tt} + 2g_{t\varphi} \Omega_\text{eff} + g_{\varphi\varphi} \Omega_\text{eff}^2 \right]"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_55(self, as_latex: bool = True) -> str:
        """Return equation 55 as LaTeX or Python string."""
        eq = r"""\begin{aligned}
  g_{tt} &\rightarrow -\left(1 - \frac{v_r^2}{c^2}\right), \\
  g_{t\varphi} &\rightarrow -\frac{v_r v_\varphi}{c^2}, \\
  g_{\varphi\varphi} &\rightarrow -\frac{v_\varphi^2}{c^2 r^2}
 \end{aligned}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_56(self, as_latex: bool = True) -> str:
        """Return equation 56 as LaTeX or Python string."""
        eq = r"""\left( \frac{d\tau}{d\mathcal{N}} \right)^2 = 1 - \frac{v_r^2}{c^2} - \frac{2v_r v_\varphi}{c^2} - \frac{v_\varphi^2}{c^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_57(self, as_latex: bool = True) -> str:
        """Return equation 57 as LaTeX or Python string."""
        eq = r"""\left( \frac{d\tau}{d\mathcal{N}} \right)^2 = 1 - \frac{1}{c^2}(v_r + v_\varphi)^2"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_58(self, as_latex: bool = True) -> str:
        """Return equation 58 as LaTeX or Python string."""
        eq = r"""\boxed{\left( \frac{d\tau}{d\mathcal{N}} \right)^2 = 1 - \frac{1}{c^2}(v_r + r\Omega_k)^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_59(self, as_latex: bool = True) -> str:
        """Return equation 59 as LaTeX or Python string."""
        eq = r"""t_{\text{adjusted}} = \Delta t \cdot \sqrt{1 - \frac{2GM}{rc^2} - \frac{J^2}{r^3c^2}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_60(self, as_latex: bool = True) -> str:
        """Return equation 60 as LaTeX or Python string."""
        eq = r"""\begin{aligned}
        \frac{2GM}{rc^2} &\rightarrow \frac{\gamma \langle \omega^2 \rangle}{r c^2}, \\
        \frac{J^2}{r^3 c^2} &\rightarrow \frac{\kappa^2}{r^3 c^2}
    \end{aligned}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_61(self, as_latex: bool = True) -> str:
        """Return equation 61 as LaTeX or Python string."""
        eq = r"""\boxed{
        \frac{d\tau}{d\bar{t}} = \sqrt{1 - \frac{\gamma \langle \omega^2 \rangle}{r c^2} - \frac{\kappa^2}{r^3 c^2}}
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_62(self, as_latex: bool = True) -> str:
        """Return equation 62 as LaTeX or Python string."""
        eq = r"""\omega_\text{drag}^\text{VAM}(r) =
    \frac{4 G m}{5 c^2 r} \cdot \mu(r) \cdot \Omega(r)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_63(self, as_latex: bool = True) -> str:
        """Return equation 63 as LaTeX or Python string."""
        eq = r"""\mu(r) =
    \begin{cases}
        \frac{r_c C_e}{r^2}, & r < r_\ast \quad \text{(quantum/vortex regime)} \\
        1, & r \geq r_\ast \quad \text{(macroscopic limit)}
    \end{cases}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_64(self, as_latex: bool = True) -> str:
        """Return equation 64 as LaTeX or Python string."""
        eq = r"""z_\text{VAM} = \left( 1 - \frac{v_\varphi^2}{c^2} \right)^{-\frac{1}{2}} - 1"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_65(self, as_latex: bool = True) -> str:
        """Return equation 65 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\bar{t}} =
    \sqrt{1 - \frac{\Omega^2 r^2}{c^2}} = \sqrt{1 - \frac{v_\varphi^2}{c^2}}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_66(self, as_latex: bool = True) -> str:
        """Return equation 66 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\mathcal{N}} =
    \left( 1 + \frac{1}{2} \cdot \beta \cdot I \cdot \Omega^2 \right)^{-1}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_67(self, as_latex: bool = True) -> str:
        """Return equation 67 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\bar{t}} =
    \sqrt{1 - \frac{v_\phi^2}{c^2}} =
    \sqrt{1 - \frac{\Omega^2 r^2}{c^2}} \quad \text{(external observer)}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_68(self, as_latex: bool = True) -> str:
        """Return equation 68 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\mathcal{N}} = \left(1 + \frac{1}{2} \cdot \beta \cdot I \cdot \Omega^2 \right)^{-1} \quad \text{(background time)}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_69(self, as_latex: bool = True) -> str:
        """Return equation 69 as LaTeX or Python string."""
        eq = r"""\boxed{
\frac{d\tau}{d\bar{t}} =
\sqrt{1 - \frac{\gamma \langle \omega^2 \rangle}{r c^2} - \frac{\kappa^2}{r^3 c^2}} \cdot
\left(1 + \frac{1}{2} \beta I \Omega^2 \right)^{-1}
}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_70(self, as_latex: bool = True) -> str:
        """Return equation 70 as LaTeX or Python string."""
        eq = r"""\boxed{
\frac{d\tau}{d\bar{t}} =
\sqrt{1 - \frac{\gamma \langle \omega^2 \rangle}{r c^2} - \frac{\kappa^2}{r^3 c^2}} \cdot
\left(1 + \frac{1}{2} \beta I \Omega_k^2 \right)^{-1}
}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_71(self, as_latex: bool = True) -> str:
        """Return equation 71 as LaTeX or Python string."""
        eq = r"""V_\text{Coulomb} = \frac{Z_1 Z_2 e^2}{4\pi \varepsilon_0 r}, \quad
    \Delta P = \frac{1}{2} \rho_\text{\ae} r_c^2 (\Omega_1^2 + \Omega_2^2)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_72(self, as_latex: bool = True) -> str:
        """Return equation 72 as LaTeX or Python string."""
        eq = r"""\Delta P \geq \frac{Z_1 Z_2 e^2}{4\pi \varepsilon_0 r_t^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_73(self, as_latex: bool = True) -> str:
        """Return equation 73 as LaTeX or Python string."""
        eq = r"""V_\text{Coulomb}(r) = \frac{Z_1 Z_2 e^2}{4\pi \varepsilon_0 r}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_74(self, as_latex: bool = True) -> str:
        """Return equation 74 as LaTeX or Python string."""
        eq = r"""\Delta P = \frac{1}{2} \rho_\text{\ae} r_c^2 (\Omega_1^2 + \Omega_2^2)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_75(self, as_latex: bool = True) -> str:
        """Return equation 75 as LaTeX or Python string."""
        eq = r"""V_\text{eff}(r) = V_\text{Coulomb}(r) - \Phi_\omega(r)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_76(self, as_latex: bool = True) -> str:
        """Return equation 76 as LaTeX or Python string."""
        eq = r"""\Phi_\omega(r) = \gamma \int \frac{|\vec{\omega}(r')|^2}{|\vec{r} - \vec{r}'|} \, d^3r',
    \quad \text{where} \quad \gamma = G \rho_\text{\ae}^2"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_77(self, as_latex: bool = True) -> str:
        """Return equation 77 as LaTeX or Python string."""
        eq = r"""\frac{1}{2} \rho_\text{\ae} r_c^2 (\Omega_1^2 + \Omega_2^2) \geq \frac{Z_1 Z_2 e^2}{4\pi \varepsilon_0 r_t^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_78(self, as_latex: bool = True) -> str:
        """Return equation 78 as LaTeX or Python string."""
        eq = r"""\mathcal{L}_\text{VAM-QED} =
    \bar{\psi} \left[ i \gamma^\mu \partial_\mu
                   - \gamma^\mu \left( \frac{C_e^2 r_c}{\lambda_c} \right) A_\mu
                   - \left( \frac{8\pi \rho_\text{\ae} r_c^3 \, \text{Lk}}{C_e} \right) \right] \psi
    - \frac{1}{4} F_{\mu\nu} F^{\mu\nu}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_79(self, as_latex: bool = True) -> str:
        """Return equation 79 as LaTeX or Python string."""
        eq = r"""\boxed{
    \left( i \gamma^\mu \partial_\mu
         - \gamma^\mu q_\text{vortex} A_\mu
         - M_\text{vortex}
    \right)\psi = 0
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_80(self, as_latex: bool = True) -> str:
        """Return equation 80 as LaTeX or Python string."""
        eq = r"""a_0 = \frac{4\pi \varepsilon_0 \hbar^2}{m_e e^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_81(self, as_latex: bool = True) -> str:
        """Return equation 81 as LaTeX or Python string."""
        eq = r"""v_\phi(r) = \frac{\Gamma}{2\pi r}, \quad \text{with} \quad \Gamma = 2\pi r_c C_e"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_82(self, as_latex: bool = True) -> str:
        """Return equation 82 as LaTeX or Python string."""
        eq = r"""v_\phi(r) = \frac{r_c C_e}{r}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_83(self, as_latex: bool = True) -> str:
        """Return equation 83 as LaTeX or Python string."""
        eq = r"""\frac{m_e v_\phi^2}{r} = \frac{e^2}{4\pi \varepsilon_0 r^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_84(self, as_latex: bool = True) -> str:
        """Return equation 84 as LaTeX or Python string."""
        eq = r"""\frac{m_e (r_c C_e)^2}{r^3} = \frac{e^2}{4\pi \varepsilon_0 r^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_85(self, as_latex: bool = True) -> str:
        """Return equation 85 as LaTeX or Python string."""
        eq = r"""a_0 = \frac{4\pi \varepsilon_0 m_e r_c^2 C_e^2}{e^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_86(self, as_latex: bool = True) -> str:
        """Return equation 86 as LaTeX or Python string."""
        eq = r"""\boxed{
        \text{Bohr radius in VAM} =
        \text{Stable tidal resonance of swirl pressure in a vortex-induced \ae ther cavity}
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_87(self, as_latex: bool = True) -> str:
        """Return equation 87 as LaTeX or Python string."""
        eq = r"""\vec{F}_\text{int} = \beta \cdot \kappa_1 \kappa_2 \cdot \frac{\vec{r}_{12} \times (\vec{v}_1 - \vec{v}_2)}{|\vec{r}_{12}|^3}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_88(self, as_latex: bool = True) -> str:
        """Return equation 88 as LaTeX or Python string."""
        eq = r"""\langle \omega^2 \rangle \sim \frac{\hbar}{\rho_\text{æ} \xi^4}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_89(self, as_latex: bool = True) -> str:
        """Return equation 89 as LaTeX or Python string."""
        eq = r"""(\vec{v} \cdot \nabla)\vec{v} = -\frac{1}{\rho} \nabla p,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_90(self, as_latex: bool = True) -> str:
        """Return equation 90 as LaTeX or Python string."""
        eq = r"""(\vec{v} \cdot \nabla)\vec{v} = \nabla\left(\frac{1}{2}v^2\right) - \vec{v} \times (\nabla \times \vec{v}) = \nabla\left(\frac{1}{2}v^2\right) - \vec{v} \times \vec{\omega},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_91(self, as_latex: bool = True) -> str:
        """Return equation 91 as LaTeX or Python string."""
        eq = r"""\nabla\left(\frac{1}{2}v^2\right) - \vec{v} \times \vec{\omega} = -\frac{1}{\rho} \nabla p."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_92(self, as_latex: bool = True) -> str:
        """Return equation 92 as LaTeX or Python string."""
        eq = r"""\vec{v} \cdot \nabla\left(\frac{1}{2}v^2 + \frac{p}{\rho}\right) = 0."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_93(self, as_latex: bool = True) -> str:
        """Return equation 93 as LaTeX or Python string."""
        eq = r"""B = \frac{1}{2}v^2 + \frac{p}{\rho}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_94(self, as_latex: bool = True) -> str:
        """Return equation 94 as LaTeX or Python string."""
        eq = r"""\vec{F}_g = -\nabla \Phi_v,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_95(self, as_latex: bool = True) -> str:
        """Return equation 95 as LaTeX or Python string."""
        eq = r"""\Phi_v(\vec{r}) = \gamma \int \frac{\|\vec{\omega}(\vec{r}')\|^2}{\|\vec{r} - \vec{r}'\|} \, d^3r',"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_96(self, as_latex: bool = True) -> str:
        """Return equation 96 as LaTeX or Python string."""
        eq = r"""\nabla^2 \Phi_v(\vec{r}) = -\rho \|\vec{\omega}(\vec{r})\|^2,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_97(self, as_latex: bool = True) -> str:
        """Return equation 97 as LaTeX or Python string."""
        eq = r"""\Phi_v(\vec{r}) = \gamma \int \frac{\|\vec{\omega}(\vec{r}')\|^2}{\|\vec{r} - \vec{r}'\|} \, d^3r',"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_98(self, as_latex: bool = True) -> str:
        """Return equation 98 as LaTeX or Python string."""
        eq = r"""\Phi_v(r) \to -\frac{G M_\text{eff}}{r},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_99(self, as_latex: bool = True) -> str:
        """Return equation 99 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} \approx \sqrt{1 - \frac{2 G_\text{swirl} M_\text{eff}}{r c^2}}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_100(self, as_latex: bool = True) -> str:
        """Return equation 100 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt}_\text{GR} \approx \sqrt{1 - \frac{2GM}{rc^2}}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_101(self, as_latex: bool = True) -> str:
        """Return equation 101 as LaTeX or Python string."""
        eq = r"""g = \frac{G M}{R^2} \approx \frac{6.674 \times 10^{-11} \cdot 5.97 \times 10^{24}}{(6.371 \times 10^6)^2} \approx 9.8 \, \text{m/s}^2."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_102(self, as_latex: bool = True) -> str:
        """Return equation 102 as LaTeX or Python string."""
        eq = r"""g = -\frac{d\Phi_v}{dr} \approx \frac{G M_\text{eff}}{R^2}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_103(self, as_latex: bool = True) -> str:
        """Return equation 103 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} = \sqrt{1 - \frac{C_e^2}{c^2} e^{-r/r_c} - \frac{2G_\text{swirl} M_\text{eff}(r)}{rc^2} - \beta \Omega^2}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_104(self, as_latex: bool = True) -> str:
        """Return equation 104 as LaTeX or Python string."""
        eq = r"""\Gamma = \oint_{\mathcal{C}(t)} \vec{v} \cdot d\vec{l} = \text{const.}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_105(self, as_latex: bool = True) -> str:
        """Return equation 105 as LaTeX or Python string."""
        eq = r"""\Gamma = \oint \vec{v} \cdot d\vec{l} = 2\pi r_c C_e."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_106(self, as_latex: bool = True) -> str:
        """Return equation 106 as LaTeX or Python string."""
        eq = r"""\Gamma_n = n \cdot \kappa, \quad n \in \mathbb{Z},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_107(self, as_latex: bool = True) -> str:
        """Return equation 107 as LaTeX or Python string."""
        eq = r"""\kappa = C_e r_c"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_108(self, as_latex: bool = True) -> str:
        """Return equation 108 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} = \left(1 + \frac{1}{2} \beta I \Omega^2 \right)^{-1},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_109(self, as_latex: bool = True) -> str:
        """Return equation 109 as LaTeX or Python string."""
        eq = r"""\frac{1}{2} \rho v^2 + p = \text{const.}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_110(self, as_latex: bool = True) -> str:
        """Return equation 110 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} \sim \frac{H_\text{ref}}{H_\text{loc}} \approx \frac{1}{1 + \frac{\Delta p}{\rho}},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_111(self, as_latex: bool = True) -> str:
        """Return equation 111 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} \approx \left(1 + \frac{1}{2} \beta I \Omega^2 \right)^{-1}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_112(self, as_latex: bool = True) -> str:
        """Return equation 112 as LaTeX or Python string."""
        eq = r"""\Phi_v(\vec{r}) = G_\text{swirl} \int \frac{\|\vec{\omega}(\vec{r}')\|^2}{\|\vec{r} - \vec{r}'\|} \, d^3r',"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_113(self, as_latex: bool = True) -> str:
        """Return equation 113 as LaTeX or Python string."""
        eq = r"""G_\text{swirl} = \frac{C_e c^5 t_p^2}{2 F^{\text{max}}_{\text{\ae}} r_c^2}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_114(self, as_latex: bool = True) -> str:
        """Return equation 114 as LaTeX or Python string."""
        eq = r"""\Phi_v(r) = G_\text{swirl} \int \frac{\|\vec{\omega}(\vec{r}')\|^2}{|\vec{r} - \vec{r}'|} d^3r' \approx \frac{G_\text{swirl}}{r} \int \|\vec{\omega}(\vec{r}')\|^2 d^3r'."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_115(self, as_latex: bool = True) -> str:
        """Return equation 115 as LaTeX or Python string."""
        eq = r"""M_\text{eff} = \frac{1}{\rho_\text{æ}} \int \rho_\text{æ} \|\vec{\omega}(\vec{r}')\|^2 d^3r' = \int \|\vec{\omega}(\vec{r}')\|^2 d^3r'."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_116(self, as_latex: bool = True) -> str:
        """Return equation 116 as LaTeX or Python string."""
        eq = r"""\Phi_v(r) \to -\frac{G_\text{swirl} M_\text{eff}}{r},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_117(self, as_latex: bool = True) -> str:
        """Return equation 117 as LaTeX or Python string."""
        eq = r"""M_\text{eff} \propto \int \frac{1}{2} \rho_\text{æ} \|\vec{v}(\vec{r})\|^2 d^3r."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_118(self, as_latex: bool = True) -> str:
        """Return equation 118 as LaTeX or Python string."""
        eq = r"""M_\text{eff} = \alpha \cdot \rho_\text{æ} C_e r_c^3 \cdot L_k,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_119(self, as_latex: bool = True) -> str:
        """Return equation 119 as LaTeX or Python string."""
        eq = r"""M_\text{eff} \overset{!}{=} M_\text{obs}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_120(self, as_latex: bool = True) -> str:
        """Return equation 120 as LaTeX or Python string."""
        eq = r"""\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p,
   \quad \nabla \cdot \mathbf{u} = 0."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_121(self, as_latex: bool = True) -> str:
        """Return equation 121 as LaTeX or Python string."""
        eq = r"""E_\text{total} \;=\; E_\text{self} \;+\; E_\text{cross}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_122(self, as_latex: bool = True) -> str:
        """Return equation 122 as LaTeX or Python string."""
        eq = r"""V \;=\; \frac{\Gamma}{4 \pi R}
   \bigl(\ln \tfrac{8 R}{a} - \beta \bigr),"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_123(self, as_latex: bool = True) -> str:
        """Return equation 123 as LaTeX or Python string."""
        eq = r"""\mathbf{u} \;=\; \mathbf{u}_1 \;+\;\mathbf{u}_2,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_124(self, as_latex: bool = True) -> str:
        """Return equation 124 as LaTeX or Python string."""
        eq = r"""E_\text{cross} \;=\; \rho \int_V \mathbf{u}_1 \cdot \mathbf{u}_2 \, dV."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_125(self, as_latex: bool = True) -> str:
        """Return equation 125 as LaTeX or Python string."""
        eq = r"""H \;=\; \int_V \mathbf{u} \cdot \boldsymbol{\omega}\, dV,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_126(self, as_latex: bool = True) -> str:
        """Return equation 126 as LaTeX or Python string."""
        eq = r"""E_\text{total}
   = \frac{\rho}{2} \int_V \left(\sum_{n=1}^N \mathbf{u}_n \right)^2 dV
   = \frac{\rho}{2} \sum_{n=1}^N \int_V \mathbf{u}_n^2 \, dV
   \;+\;\rho \sum_{n<m} \int_V \mathbf{u}_n \cdot \mathbf{u}_m \, dV."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_127(self, as_latex: bool = True) -> str:
        """Return equation 127 as LaTeX or Python string."""
        eq = r"""E_\text{cross}^{(ij)} \;=\; \rho \int_V \mathbf{u}_i \cdot \mathbf{u}_j \, dV."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_128(self, as_latex: bool = True) -> str:
        """Return equation 128 as LaTeX or Python string."""
        eq = r"""\Delta U = Q - W,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_129(self, as_latex: bool = True) -> str:
        """Return equation 129 as LaTeX or Python string."""
        eq = r"""\Delta U = \Delta \left( \frac{1}{2} \rho_\text{\ae} \int v^2 \, dV + \int P \, dV \right),"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_130(self, as_latex: bool = True) -> str:
        """Return equation 130 as LaTeX or Python string."""
        eq = r"""S \propto \int \omega^2 \, dV,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_131(self, as_latex: bool = True) -> str:
        """Return equation 131 as LaTeX or Python string."""
        eq = r"""W = \frac{1}{2} \rho_\text{\ae} \int v^2 \, dV + P_\text{eq} V_\text{eq},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_132(self, as_latex: bool = True) -> str:
        """Return equation 132 as LaTeX or Python string."""
        eq = r"""F^{\text{max}}_{\text{\ae}} = \rho_\text{\ae} C_e^2 \pi r_c^2,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_133(self, as_latex: bool = True) -> str:
        """Return equation 133 as LaTeX or Python string."""
        eq = r"""\vec{\omega} = \nabla \times \vec{v}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_134(self, as_latex: bool = True) -> str:
        """Return equation 134 as LaTeX or Python string."""
        eq = r"""H_\text{vortex} = \frac{1}{(4\pi)^2} \int_{\mathbb{R}^3} \vec{v} \cdot \vec{\omega} \, d^3x."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_135(self, as_latex: bool = True) -> str:
        """Return equation 135 as LaTeX or Python string."""
        eq = r"""Q_\text{top} = \frac{L}{(4\pi)^2 \Gamma^2} \int \vec{v} \cdot \vec{\omega} \, d^3x,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_136(self, as_latex: bool = True) -> str:
        """Return equation 136 as LaTeX or Python string."""
        eq = r"""\mathcal{L}_\text{top} = \frac{C_e^2}{2} \rho_\text{\ae} \, \vec{v} \cdot \vec{\omega},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_137(self, as_latex: bool = True) -> str:
        """Return equation 137 as LaTeX or Python string."""
        eq = r"""\mathcal{E}_\text{VAM} = \int \left[
                                        \frac{1}{2} \rho_\text{\ae} |\vec{v}|^2
        + \frac{C_e^2}{2} \rho_\text{\ae} \, \vec{v} \cdot \vec{\omega}
                                        + \Phi_\text{swirl} + P(\rho_\text{\ae})
    \right] d^3x."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_138(self, as_latex: bool = True) -> str:
        """Return equation 138 as LaTeX or Python string."""
        eq = r"""\mathcal{E}_\text{micro} = \int_V \left[
                                            A |\nabla \vec{m}|^2 + D \vec{m} \cdot (\nabla \times \vec{m}) - \mu_0 \vec{M} \cdot \vec{B} + \frac{1}{2\mu_0} |\nabla \vec{A}_d|^2
    \right] d^3x,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_139(self, as_latex: bool = True) -> str:
        """Return equation 139 as LaTeX or Python string."""
        eq = r"""\vec{v} \cdot \vec{\omega} \sim \vec{m} \cdot (\nabla \times \vec{m}),"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_140(self, as_latex: bool = True) -> str:
        """Return equation 140 as LaTeX or Python string."""
        eq = r"""H_\text{vortex} = n H_0, \quad n \in \mathbb{Z},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_141(self, as_latex: bool = True) -> str:
        """Return equation 141 as LaTeX or Python string."""
        eq = r"""dt = dt_\infty \sqrt{1 - \frac{U_\text{vortex}}{U_\text{max}}},
    \quad \text{met} \quad
    U_\text{vortex} = \frac{1}{2} \rho_\text{\ae} |\vec{\omega}|^2."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_142(self, as_latex: bool = True) -> str:
        """Return equation 142 as LaTeX or Python string."""
        eq = r"""H = H_C + H_T,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_143(self, as_latex: bool = True) -> str:
        """Return equation 143 as LaTeX or Python string."""
        eq = r"""\text{Wr} = \frac{1}{4\pi} \int_C \int_C \frac{\left(\vec{T}(s) \times \vec{T}(s')\right) \cdot \left(\vec{r}(s) - \vec{r}(s')\right)}{|\vec{r}(s) - \vec{r}(s')|^3} \, ds \, ds',"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_144(self, as_latex: bool = True) -> str:
        """Return equation 144 as LaTeX or Python string."""
        eq = r"""dt = dt_\infty \sqrt{1 - \frac{H_C + H_T}{H_\text{max}}} = dt_\infty \sqrt{1 - \frac{C^2 (\text{Wr} + \text{Tw})}{H_\text{max}}}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_145(self, as_latex: bool = True) -> str:
        """Return equation 145 as LaTeX or Python string."""
        eq = r"""\mathcal{L}_\text{VAM}[\psi] =
    \frac{i\hbar}{2} \left( \psi^\dagger \partial_t \psi - \psi \partial_t \psi^\dagger \right)
    - \frac{\hbar^2}{2m} |\nabla \psi|^2
    - \frac{\alpha}{8} |\nabla \vec{s}|^2,"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_146(self, as_latex: bool = True) -> str:
        """Return equation 146 as LaTeX or Python string."""
        eq = r"""\Gamma = \oint \vec{v} \cdot d\vec{\ell} = \frac{h}{m_e} = \frac{2\pi \hbar}{m_e}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_147(self, as_latex: bool = True) -> str:
        """Return equation 147 as LaTeX or Python string."""
        eq = r"""\Gamma = 2\pi r_c C_e."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_148(self, as_latex: bool = True) -> str:
        """Return equation 148 as LaTeX or Python string."""
        eq = r"""2\pi r_c C_e = \frac{2\pi \hbar}{m_e} \quad \Rightarrow \quad C_e = \frac{\hbar}{m_e r_c}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_149(self, as_latex: bool = True) -> str:
        """Return equation 149 as LaTeX or Python string."""
        eq = r"""R_e = \frac{e^2}{4\pi \varepsilon_0 m_e c^2}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_150(self, as_latex: bool = True) -> str:
        """Return equation 150 as LaTeX or Python string."""
        eq = r"""C_e = \frac{\hbar}{m_e \cdot \frac{R_e}{2}} = \frac{2\hbar}{m_e R_e}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_151(self, as_latex: bool = True) -> str:
        """Return equation 151 as LaTeX or Python string."""
        eq = r"""C_e = \frac{2\hbar}{m_e} \cdot \frac{4\pi \varepsilon_0 m_e c^2}{e^2} = \frac{8\pi \varepsilon_0 \hbar c^2}{e^2}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_152(self, as_latex: bool = True) -> str:
        """Return equation 152 as LaTeX or Python string."""
        eq = r"""\alpha = \frac{e^2}{4\pi \varepsilon_0 \hbar c},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_153(self, as_latex: bool = True) -> str:
        """Return equation 153 as LaTeX or Python string."""
        eq = r"""\frac{1}{\alpha} = \frac{4\pi \varepsilon_0 \hbar c}{e^2}."""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_154(self, as_latex: bool = True) -> str:
        """Return equation 154 as LaTeX or Python string."""
        eq = r"""\boxed{
        \alpha = \frac{2 C_e}{c}
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_155(self, as_latex: bool = True) -> str:
        """Return equation 155 as LaTeX or Python string."""
        eq = r"""\boxed{
        \frac{d\tau}{d\mathcal{N}} = \sqrt{
            1
            - \frac{2 G_{\text{hybrid}}(r) M_{\text{hybrid}}(r)}{r c^2}
            - \frac{C_e^2}{c^2} e^{-r/r_c}
            - \frac{C_e^2}{r_c^2 c^2} e^{-r/r_c}
        }}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_156(self, as_latex: bool = True) -> str:
        """Return equation 156 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} = \sqrt{
        1
        - \frac{C_e^2}{c^2} e^{-r/r_c}
        - \frac{2 G_\text{swirl} M_\text{eff}(r)}{r c^2}
        - \beta \Omega^2
    }"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_157(self, as_latex: bool = True) -> str:
        """Return equation 157 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{dt} = \left(1 + \frac{1}{2} \beta I \Omega^2 \right)^{-1},"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_158(self, as_latex: bool = True) -> str:
        """Return equation 158 as LaTeX or Python string."""
        eq = r"""\Phi(r) = \frac{C_e^3}{2 F_{\text{max}} r_c} \cdot r e^{-r / r_c}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_159(self, as_latex: bool = True) -> str:
        """Return equation 159 as LaTeX or Python string."""
        eq = r"""\Delta \Phi \sim \frac{C_e^3}{2 F_{\text{max}} r_c} \Rightarrow \Delta g = -\dv{\Phi}{r} \sim A e^{-r/r_c} \left(1 - \frac{r}{r_c}\right)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_160(self, as_latex: bool = True) -> str:
        """Return equation 160 as LaTeX or Python string."""
        eq = r"""\Delta g(r) = -\dv{\Phi}{r} = -\frac{C_e^3}{2 F_{\text{max}} r_c^2} \left(1 - \frac{r}{r_c}\right) e^{-r/r_c}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_161(self, as_latex: bool = True) -> str:
        """Return equation 161 as LaTeX or Python string."""
        eq = r"""\frac{d\tau}{d\mathcal{N}} = \gamma^{-1}(\vec{v})"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_162(self, as_latex: bool = True) -> str:
        """Return equation 162 as LaTeX or Python string."""
        eq = r"""\nabla S(t) = \frac{\partial \vec{S}}{\partial \mathcal{N}} + \omega(\tau)\hat{n}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_163(self, as_latex: bool = True) -> str:
        """Return equation 163 as LaTeX or Python string."""
        eq = r"""F^{\mu\nu}(\Xi_0) = \partial^\mu A^\nu - \partial^\nu A^\mu + \phi(\circlearrowleft)\delta^{\mu\nu}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_164(self, as_latex: bool = True) -> str:
        """Return equation 164 as LaTeX or Python string."""
        eq = r"""\Sigma_{\nu_0} = \{ x^\mu \mid \tau(x) = \mathcal{N} \}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_165(self, as_latex: bool = True) -> str:
        """Return equation 165 as LaTeX or Python string."""
        eq = r"""\frac{dE}{d\mathcal{N}} + \nabla \cdot \vec{J} = \mathbb{K}(\vec{x}, \tau)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_166(self, as_latex: bool = True) -> str:
        """Return equation 166 as LaTeX or Python string."""
        eq = r"""\frac{dE}{d\mathcal{N}} + \nabla \cdot \vec{J} = \mathbb{K}(\vec{x}, \tau)"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_167(self, as_latex: bool = True) -> str:
        """Return equation 167 as LaTeX or Python string."""
        eq = r"""\nabla \vec{S}(t) = \frac{d}{d\mathcal{N}} \vec{S}(t) + \omega(\tau) \hat{n}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_168(self, as_latex: bool = True) -> str:
        """Return equation 168 as LaTeX or Python string."""
        eq = r"""F^{\mu\nu} = \partial^\mu A^\nu - \partial^\nu A^\mu + \phi(\circlearrowleft) \delta^{\mu\nu}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_169(self, as_latex: bool = True) -> str:
        """Return equation 169 as LaTeX or Python string."""
        eq = r"""\boxed{
    \frac{d\tau}{d\mathcal{N}} = \sqrt{1 - \frac{|\vec{v}_\theta|^2}{c^2}}
} \quad \text{with} \quad |\vec{v}_\theta| = |\vec{\omega}| r"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_170(self, as_latex: bool = True) -> str:
        """Return equation 170 as LaTeX or Python string."""
        eq = r"""\boxed{
    T_v = \oint \frac{ds}{v_\text{phase}}
}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_171(self, as_latex: bool = True) -> str:
        """Return equation 171 as LaTeX or Python string."""
        eq = r"""\boxed{
    \nabla S(t) = \frac{dS}{d\mathcal{N}} + \vec{\omega}(\tau) \cdot \hat{n}
}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_172(self, as_latex: bool = True) -> str:
        """Return equation 172 as LaTeX or Python string."""
        eq = r"""\boxed{
    ds^2 = C_e^2 dT_v^2 - dr^2
}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

    def equation_173(self, as_latex: bool = True) -> str:
        """Return equation 173 as LaTeX or Python string."""
        eq = r"""\boxed{
    \frac{d\tau}{d\mathcal{N}} = \sqrt{1 - \frac{\Gamma^2}{4\pi^2 r^2 c^2}}
}"""
        if as_latex:
            return eq
        return latex_to_python(eq)

