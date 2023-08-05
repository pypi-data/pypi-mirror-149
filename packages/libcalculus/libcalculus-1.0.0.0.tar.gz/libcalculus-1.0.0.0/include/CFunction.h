#pragma once
#include <iostream>
#include <iomanip>
#include <complex>
#include <functional>
#include <string>
#include <sstream>
#include <regex>
#include "Definitions.h"
#include "Latex.h"
#include "CComparison.h"

namespace libcalculus {
    #define LATEX_VAR "%var"

    template <typename Dom, typename Ran>
    class CFunction {
        using function = std::function<Ran(Dom)>;
    private:
        function _f = [](Dom z) noexcept { return z; };
        std::string _latex = LATEX_VAR;
        OP_TYPE _last_op = OP_TYPE::NOP;
        template<typename, typename> friend class CFunction;
        template<typename Dom_, typename Ran_> friend CFunction<Dom_, Ran_> Derivative(CFunction<Dom_, Ran_> const &f, size_t const order, REAL const tol, REAL const radius);
        template<typename Dom_, typename Ran_, typename ContDom_>
        friend Ran_ Integrate(CFunction<Dom_, Ran_> const &f, CFunction<ContDom_, Dom_> const &contour, ContDom_ const start, ContDom_ const End, double const tol);

        /* Preset instances */
        static CFunction const _Identity;
        static CFunction const _Re;
        static CFunction const _Im;
        static CFunction const _Conj;
        static CFunction const _Abs;
        static CFunction const _Arg;
        static CFunction const _Exp;
        static CFunction const _Ln;
        static CFunction const _Sin;
        static CFunction const _Cos;
        static CFunction const _Tan;
        static CFunction const _Sec;
        static CFunction const _Csc;
        static CFunction const _Cot;
        static CFunction const _Sinh;
        static CFunction const _Cosh;
        static CFunction const _Tanh;
        static CFunction const _Sech;
        static CFunction const _Csch;
        static CFunction const _Coth;
        static CFunction const _Arcsin;
        static CFunction const _Arccos;
        static CFunction const _Arctan;
        static CFunction const _Arccsc;
        static CFunction const _Arcsec;
        static CFunction const _Arccot;
        static CFunction const _Arsinh;
        static CFunction const _Arcosh;
        static CFunction const _Artanh;
        static CFunction const _Arcsch;
        static CFunction const _Arsech;
        static CFunction const _Arcoth;
        static CFunction const _Pi;
        static CFunction const _E;

    public:
        CFunction() {}
        CFunction(CFunction const &cf) : _f{cf._f}, _latex{cf._latex}, _last_op{cf._last_op} {}
        CFunction(function const &f) : _f{f} {}
        CFunction(function const &f, std::string const &latex, OP_TYPE const last_op) : _f{f}, _latex{latex}, _last_op{last_op} {}
        inline Ran operator()(Dom z) const { return this->_f(z); };
        void operator()(Dom const *RESTRICT z, Ran *RESTRICT result, size_t const n) const;
        std::string latex(std::string const &varname = "z") const;

        /* Function composition */
        template<typename Predom> CFunction<Predom, Ran> compose(CFunction<Predom, Dom> const &rhs) const;

        /* In-place function-with-function operators */
        CFunction &operator+=(CFunction const &rhs);
        CFunction &operator-=(CFunction const &rhs);
        CFunction &operator*=(CFunction const &rhs);
        CFunction &operator/=(CFunction const &rhs);
        CFunction &ipow(CFunction<Dom, Ran> const &rhs);

        /* In-place function-with-constant operators */
        CFunction &operator+=(Ran const c);
        CFunction &operator-=(Ran const c);
        CFunction &operator*=(Ran const c);
        CFunction &operator/=(Ran const c);
        CFunction &ipow(Ran const c);

        /* Function additive inverse */
        CFunction operator-() const;

        /* Function-with-function operators */
        inline CFunction operator+(CFunction const &rhs) const { return CFunction(*this) += rhs; }
        inline CFunction operator-(CFunction const &rhs) const { return CFunction(*this) -= rhs; }
        inline CFunction operator*(CFunction const &rhs) const { return CFunction(*this) *= rhs; }
        inline CFunction operator/(CFunction const &rhs) const { return CFunction(*this) /= rhs; }
        CFunction pow(CFunction const &rhs) const;

        /* Function-with-constant operators */
        template<typename Dom_, typename Ran_> friend CFunction<Dom_, Ran_> operator+(CFunction<Dom_, Ran_> const &lhs, Ran const rhs);
        template<typename Dom_, typename Ran_> friend CFunction<Dom_, Ran_> operator-(CFunction<Dom_, Ran_> const &lhs, Ran const rhs);
        template<typename Dom_, typename Ran_> friend CFunction<Dom_, Ran_> operator*(CFunction<Dom_, Ran_> const &lhs, Ran const rhs);
        template<typename Dom_, typename Ran_> friend CFunction<Dom_, Ran_> operator/(CFunction<Dom_, Ran_> const &lhs, Ran const rhs);
        CFunction pow(Ran const c) const;

        /* Constant-with-function operators */
        template<typename Dom_, typename Ran_> friend CFunction<Dom_, Ran_> operator-(Ran_ lhs, CFunction<Dom_, Ran_> const &rhs);
        template<typename Dom_, typename Ran_> friend CFunction<Dom_, Ran_> operator/(Ran_ lhs, CFunction<Dom_, Ran_> const &rhs);
        CFunction lpow(Ran const c) const;

        /* Comparison operators */
        CComparison<Dom> operator>(CFunction const &rhs) const;
        CComparison<Dom> operator<(CFunction const &rhs) const;
        CComparison<Dom> operator==(CFunction const &rhs) const;
        CComparison<Dom> operator>=(CFunction const &rhs) const;
        CComparison<Dom> operator<=(CFunction const &rhs) const;
        CComparison<Dom> operator!=(CFunction const &rhs) const;

        /* Preset instances */
        static inline CFunction Identity() { return CFunction::_Identity;  }
        static inline CFunction Constant(Ran const c) { return CFunction([=](Dom z) noexcept { return c; }, Latex::fmt_const(c, false), OP_TYPE::CONST); }
        static inline CFunction Re() { return CFunction::_Re;  }
        static inline CFunction Im() { return CFunction::_Im; }
        static inline CFunction Conj() { return CFunction::_Conj; }
        static inline CFunction Abs() { return CFunction::_Abs; }
        static inline CFunction Arg() { return CFunction::_Arg; }
        static inline CFunction Exp() { return CFunction::_Exp; }
        static inline CFunction Ln() { return CFunction::_Ln; }
        static inline CFunction Sin() { return CFunction::_Sin; }
        static inline CFunction Cos() { return CFunction::_Cos; }
        static inline CFunction Tan() { return CFunction::_Tan; }
        static inline CFunction Sec() { return CFunction::_Sec; }
        static inline CFunction Csc() { return CFunction::_Csc; }
        static inline CFunction Cot() { return CFunction::_Cot; }

        static inline CFunction Sinh() { return CFunction::_Sinh; }
        static inline CFunction Cosh() { return CFunction::_Cosh; }
        static inline CFunction Tanh() { return CFunction::_Tanh; }
        static inline CFunction Sech() { return CFunction::_Sech; }
        static inline CFunction Csch() { return CFunction::_Csch; }
        static inline CFunction Coth() { return CFunction::_Coth; }

        static inline CFunction Arcsin() { return CFunction::_Arcsin; }
        static inline CFunction Arccos() { return CFunction::_Arccos; }
        static inline CFunction Arctan() { return CFunction::_Arctan; }
        static inline CFunction Arcsec() { return CFunction::_Arcsec; }
        static inline CFunction Arccsc() { return CFunction::_Arccsc; }
        static inline CFunction Arccot() { return CFunction::_Arccot; }

        static inline CFunction Arsinh() { return CFunction::_Arsinh; }
        static inline CFunction Arcosh() { return CFunction::_Arcosh; }
        static inline CFunction Artanh() { return CFunction::_Artanh; }
        static inline CFunction Arsech() { return CFunction::_Arsech; }
        static inline CFunction Arcsch() { return CFunction::_Arcsch; }
        static inline CFunction Arcoth() { return CFunction::_Arcoth; }

        static inline CFunction Pi() { return CFunction::_Pi; }
        static inline CFunction E() { return CFunction::_E; }
        static inline CFunction If(CComparison<Dom> const &cond_, CFunction const &then_,
                                      CFunction const &else_ = CFunction::Constant(Ran{0})) {
              std::string new_latex = "\\begin{cases} ";
              new_latex.append(then_._latex);
              new_latex.append(" & ;\\;");
              new_latex.append(cond_.latex);
              new_latex.append(" \\\\ ");
              new_latex.append(else_._latex);
              new_latex.append(" & ;\\;\\text{else}\\end{cases} ");
              return CFunction([cond__ = cond_.eval, then__ = then_._f, else__ = else_._f](Dom const z) noexcept { return cond__(z) ? then__(z) : else__(z); },
                               new_latex, OP_TYPE::IF);
        }
    };

    /* Preset instances - instantiation */
    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Identity = CFunction<Dom, Ran>([](Dom const z) noexcept { return z; }, "\\text{Re}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Re = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::real(z); }, "\\text{Re}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Im = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::imag(z); }, "\\text{Im}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Conj = CFunction<Dom, Ran>(([]() constexpr {
                                                                                                if constexpr (std::is_same<Ran, COMPLEX>::value)
                                                                                                    return [](Dom const z) noexcept { return std::conj(z); };
                                                                                                else
                                                                                                    return [](Dom const z) noexcept { return z; };
                                                                                              })(), "\\overline{" LATEX_VAR "}", OP_TYPE::NOP);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Abs = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::abs(z); }, "\\left|" LATEX_VAR "\\right|", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arg = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::arg(z); }, "\\text{arg}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Exp = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::exp(z); }, "e^{" LATEX_VAR "}", OP_TYPE::NOP);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Ln = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::log(z); }, "\\text{ln}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Sin = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::sin(z); }, "\\sin\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Cos = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::cos(z); }, "\\cos\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Tan = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::tan(z); }, "\\tan\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Sec = CFunction<Dom, Ran>([](Dom const z) noexcept { return 1. / std::cos(z); }, "\\sec\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Csc = CFunction<Dom, Ran>([](Dom const z) noexcept { return 1. / std::sin(z); }, "\\csc\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Cot = CFunction<Dom, Ran>([](Dom const z) noexcept { return 1. / std::tan(z); }, "\\cot\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Sinh = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::sinh(z); }, "\\sinh\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Cosh = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::cosh(z); }, "\\cosh\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Tanh = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::tanh(z); }, "\\tanh\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Sech = CFunction<Dom, Ran>([](Dom const z) noexcept { return 1. / std::cosh(z); }, "\\text{sech}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Csch = CFunction<Dom, Ran>([](Dom const z) noexcept { return 1. / std::sinh(z); }, "\\text{csch}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Coth = CFunction<Dom, Ran>([](Dom const z) noexcept { return 1. / std::tanh(z); }, "\\coth\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arcsin = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::asin(z); }, "\\text{arcsin}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arccos = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::acos(z); }, "\\text{arccos}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arctan = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::atan(z); }, "\\text{arctan}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arccsc = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::asin(1. / z); }, "\\text{arccsc}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arcsec = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::acos(1. / z); }, "\\text{arcsec}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arccot = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::atan(1. / z); }, "\\text{arccot}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arsinh = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::asinh(z); }, "\\text{arsinh}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arcosh = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::acosh(z); }, "\\text{arcosh}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Artanh = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::atanh(z); }, "\\text{artanh}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arcsch = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::asinh(1. / z); }, "\\text{arcsch}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arsech = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::acosh(1. / z); }, "\\text{arsech}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Arcoth = CFunction<Dom, Ran>([](Dom const z) noexcept { return std::atanh(1. / z); }, "\\text{arcoth}\\left(" LATEX_VAR "\\right)", OP_TYPE::FUNC);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_Pi = CFunction<Dom, Ran>([](Dom const z) noexcept { return M_PI; }, "\\pi", OP_TYPE::NOP);

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> const CFunction<Dom, Ran>::_E = CFunction<Dom, Ran>([](Dom const z) noexcept { return M_E; }, "e", OP_TYPE::NOP);

}
