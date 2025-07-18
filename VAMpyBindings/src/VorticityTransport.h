#ifndef VAMCORE_VORTICITYTRANSPORT_H
#define VAMCORE_VORTICITYTRANSPORT_H

#pragma once
#include <array>

namespace cam {

using Vec3 = std::array<double, 3>;

class VorticityTransport {
public:
    static Vec3 baroclinic_term(const Vec3& grad_rho, const Vec3& grad_p, double rho);
    static Vec3 compute_rhs(const Vec3& omega, const std::array<Vec3, 3>& grad_u,
                            double div_u, const Vec3& grad_rho, const Vec3& grad_p, double rho);
};

}


#endif