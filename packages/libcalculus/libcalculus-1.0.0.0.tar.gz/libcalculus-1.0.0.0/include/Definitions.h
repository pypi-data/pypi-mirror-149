#pragma once
#include <complex>

#if defined(_WIN32) || defined(WIN32)
#define RESTRICT __restrict
#elif defined(__unix__)
#define RESTRICT __restrict__
#endif

namespace libcalculus {
    using namespace std::complex_literals;
    enum OP_TYPE {
        NOP, // Nothing
        CONST, // Constant
        FUNC, // Applying a function - sin, cos, etc.
        COMP, // Function composition
        ADD, // Addition: (f, g) -> f + g
        SUB, // Subtraction: (f, g) -> f - g
        MUL, // Multiplication: (f, g) -> f * g
        DIV, // Division: (f, g) -> f / g
        LPOW, // Power base: (f, g) -> f ^ g
        RPOW, // Power exponent: (g, f) -> f ^ g
        MULCONST, // Multiplication by a constant: (f, a) -> a * f
        NEG, // Negation: f -> -f
        IF, // Cases
    };

    using REAL = double;
    using COMPLEX = std::complex<double>;
    static inline double constexpr INTEGRATION_SUBDIV_FACTOR = .05; // With integration tolerance tol, the domain will
                                                                    // divided into INTEGRATION_SUBDIV_FACTOR / tol rectangles.

    template<typename T>
    struct Traits {
    public:
        static constexpr REAL tol = [] {
            if constexpr (std::is_same<T, REAL>::value)
                return 1e-6;
            else if constexpr (std::is_same<T, COMPLEX>::value)
                return 1e-6;
        }();

        inline static bool close(T const a, T const b, REAL const tol=Traits<T>::tol) noexcept { return std::abs(a - b) < tol; }
    };
}
