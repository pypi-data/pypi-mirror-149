#include "CFunction.h"

namespace libcalculus {
    template<typename Dom, typename Ran>
    void CFunction<Dom, Ran>::operator()(Dom const *RESTRICT z, Ran *RESTRICT result, size_t const n) const {
        #pragma omp simd
        for (size_t i = 0; i < n; ++i) {
            result[i] = this->_f(z[i]);
        }
    }

    template<typename Dom, typename Ran>
    std::string CFunction<Dom, Ran>::latex(std::string const &varname) const {
        return std::regex_replace(this->_latex, std::regex(LATEX_VAR), varname);
    }

    template<typename Dom, typename Ran>
    template<typename Predom>
    CFunction<Predom, Ran> CFunction<Dom, Ran>::compose(CFunction<Predom, Dom> const &rhs) const {
        std::string new_latex = std::regex_replace(this->_latex, std::regex(LATEX_VAR),
                                                   Latex::parenthesize_if(rhs._latex, OP_TYPE::COMP, rhs._last_op));
        return CFunction<Predom, Ran>([lhs_f = this->_f, rhs_f = rhs._f](Predom z) { return lhs_f(rhs_f(z)); }, new_latex, this->_last_op);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator+=(CFunction<Dom, Ran> const &rhs) {
        this->_f = [lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) + rhs_f(z); };
        this->_latex = Latex::parenthesize_if(this->_latex, OP_TYPE::ADD, this->_last_op);
        this->_latex.append(" + ");
        this->_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::ADD, rhs._last_op));
        this->_last_op = OP_TYPE::ADD;
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator-=(CFunction<Dom, Ran> const &rhs) {
        this->_f = [lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) - rhs_f(z); };
        this->_latex = Latex::parenthesize_if(this->_latex, OP_TYPE::SUB, this->_last_op);
        this->_latex.append(" - ");
        this->_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::SUB, rhs._last_op));
        this->_last_op = OP_TYPE::SUB;
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator*=(CFunction<Dom, Ran> const &rhs) {
        this->_f = [lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) * rhs_f(z); };
        this->_latex = Latex::parenthesize_if(this->_latex, OP_TYPE::MUL, this->_last_op);
        this->_latex.append((rhs._last_op == OP_TYPE::MULCONST || rhs._last_op == OP_TYPE::CONST) ? " \\cdot ": " ");
        this->_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::MUL, rhs._last_op));
        this->_last_op = this->_last_op == OP_TYPE::CONST || this->_last_op == OP_TYPE::MULCONST ? OP_TYPE::MULCONST : OP_TYPE::MUL;
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator/=(CFunction<Dom, Ran> const &rhs) {
        this->_f = [lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) / rhs_f(z); };
        std::string new_latex = " \\frac{";
        new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::DIV, this->_last_op));
        new_latex.append("}{");
        new_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::DIV, rhs._last_op));
        new_latex.append("}");
        this->_latex = new_latex;
        this->_last_op = OP_TYPE::DIV;
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::ipow(CFunction<Dom, Ran> const &rhs) {
        this->_f = [lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return std::pow(lhs_f(z), rhs_f(z)); };
        std::string new_latex = "{";
        new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::LPOW, this->_last_op));
        new_latex.append("}^{");
        new_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::RPOW, rhs._last_op));
        new_latex.append("}");
        this->_latex = new_latex;
        this->_last_op = OP_TYPE::LPOW;
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator+=(Ran const c) {
        if (!Traits<Ran>::close(c, 0)) {
            this->_f = [c = c, old_f = this->_f](Dom const z) noexcept { return old_f(z) + c; };
            this->_latex.append(" + ");
            this->_latex.append(Latex::fmt_const(c, true));
            this->_last_op = OP_TYPE::ADD;
        }
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator-=(Ran const c) {
        if (!Traits<Ran>::close(c, 0)) {
            this->_f = [c = c, old_f = this->_f](Dom const z) noexcept { return old_f(z) - c; };
            this->_latex.append(" - ");
            this->_latex.append(Latex::fmt_const(c, true));
            this->_last_op = OP_TYPE::SUB;
        }
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator*=(Ran const c) {
        if (!Traits<Ran>::close(c, 1)) {
            this->_f = [c = c, old_f = this->_f](Dom const z) noexcept { return c * old_f(z); };
            std::string new_latex = Latex::fmt_const(c, true);
            new_latex.append((this->_last_op == OP_TYPE::MULCONST || this->_last_op == OP_TYPE::CONST) ? " \\cdot " : " ");
            new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::MUL, this->_last_op));
            this->_latex = new_latex;
            this->_last_op = OP_TYPE::MULCONST;
        }
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::operator/=(Ran const c) {
        if (!Traits<Ran>::close(c, 1)) {
            this->_f = [c = c, old_f = this->_f](Dom const z) noexcept { return old_f(z) / c; };
            std::string new_latex = " \\frac{";
            new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::DIV, this->_last_op));
            new_latex.append("}{");
            new_latex.append(Latex::fmt_const(c, false));
            new_latex.append("}");
            this->_latex = new_latex;
            this->_last_op = OP_TYPE::DIV;
        }
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> &CFunction<Dom, Ran>::ipow(Ran const c) {
        this->_f = [lhs_f = this->_f, c = c](Dom const z) noexcept { return std::pow(lhs_f(z), c); };
        std::string new_latex = "{";
        new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::LPOW, this->_last_op));
        new_latex.append("}^{");
        new_latex.append(Latex::fmt_const(c, false));
        new_latex.append("}");
        this->_latex = new_latex;
        this->_last_op = OP_TYPE::LPOW;
        return *this;
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> CFunction<Dom, Ran>::operator-() const {
        std::string new_latex = "-";
        new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::NEG, this->_last_op));
        return CFunction<Dom, Ran>([old_f = this->_f](Dom const z) noexcept { return -old_f(z); }, new_latex, OP_TYPE::NEG);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> CFunction<Dom, Ran>::pow(CFunction const &rhs) const {
        std::string new_latex = "{";
        new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::LPOW, this->_last_op));
        new_latex.append("}^{");
        new_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::RPOW, rhs._last_op));
        new_latex.append("}");
        return CFunction<Dom, Ran>([lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return std::pow(lhs_f(z), rhs_f(z)); }, new_latex, OP_TYPE::LPOW);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> operator+(CFunction<Dom, Ran> const &lhs, Ran const c) {
        std::string new_latex = lhs._latex;
        new_latex.append(" + ");
        new_latex.append(Latex::fmt_const(c, true));
        return CFunction<Dom, Ran>([c = c, lhs_f = lhs._f](Dom const z) noexcept { return lhs_f(z) + c; }, new_latex, OP_TYPE::ADD);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> operator-(CFunction<Dom, Ran> const &lhs, Ran const c) {
        std::string new_latex = lhs._latex;
        new_latex.append(" - ");
        new_latex.append(Latex::fmt_const(c, true));
        return CFunction<Dom, Ran>([c = c, lhs_f = lhs._f](Dom const z) noexcept { return lhs_f(z) - c; }, new_latex, OP_TYPE::SUB);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> operator*(CFunction<Dom, Ran> const &lhs, Ran const c) {
        std::string new_latex = Latex::fmt_const(c, true);
        new_latex.append(lhs._last_op == OP_TYPE::MULCONST ? " \\cdot " : " ");
        new_latex.append(Latex::parenthesize_if(lhs._latex, OP_TYPE::MUL, lhs._last_op));
        return CFunction<Dom, Ran>([c = c, lhs_f = lhs._f](Dom const z) noexcept { return lhs_f(z) * c; }, new_latex, OP_TYPE::MULCONST);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> operator/(CFunction<Dom, Ran> const &lhs, Ran const c) {
        std::string new_latex = " \\frac{";
        new_latex.append(Latex::parenthesize_if(lhs._latex, OP_TYPE::DIV, lhs._last_op));
        new_latex.append("}{");
        new_latex.append(Latex::fmt_const(c, false));
        new_latex.append("}");
        return CFunction<Dom, Ran>([c = c, lhs_f = lhs._f](Dom const z) noexcept { return lhs_f(z) / c; }, new_latex, OP_TYPE::DIV);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> operator-(Ran const c, CFunction<Dom, Ran> const &rhs) {
        std::string new_latex = Latex::fmt_const(c, false);
        new_latex.append(" - ");
        new_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::SUB, rhs._last_op));
        return CFunction<Dom, Ran>([c = c, rhs_f = rhs._f](Dom const z) noexcept { return c - rhs_f(z); }, new_latex, OP_TYPE::SUB);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> operator/(Ran const c, CFunction<Dom, Ran> const &rhs) {
        std::string new_latex = " \\frac{";
        new_latex.append(Latex::fmt_const(c, false));
        new_latex.append("}{");
        new_latex.append(Latex::parenthesize_if(rhs._latex, OP_TYPE::DIV, rhs._last_op));
        new_latex.append("}");
        return CFunction<Dom, Ran>([c = c, rhs_f = rhs._f](Dom const z) noexcept { return c / rhs_f(z); }, new_latex, OP_TYPE::DIV);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> CFunction<Dom, Ran>::pow(Ran const c) const {
        std::string new_latex = "{";
        new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::LPOW, this->_last_op));
        new_latex.append("}^{");
        new_latex.append(Latex::fmt_const(c, false));
        new_latex.append("}");
        return CFunction<Dom, Ran>([c = c, old_f = this->_f](Dom const z) noexcept { return std::pow(old_f(z), c); }, new_latex, OP_TYPE::LPOW);
    }

    template<typename Dom, typename Ran>
    CFunction<Dom, Ran> CFunction<Dom, Ran>::lpow(Ran const c) const {
        std::string new_latex = "{";
        new_latex.append(Latex::fmt_const(c, true));
        new_latex.append("}^{");
        new_latex.append(Latex::parenthesize_if(this->_latex, OP_TYPE::LPOW, this->_last_op));
        new_latex.append("}");
        return CFunction<Dom, Ran>([c = c, old_f = this->_f](Dom const z) noexcept { return std::pow(c, old_f(z)); }, new_latex, OP_TYPE::LPOW);
    }

    template<typename Dom, typename Ran>
    CComparison<Dom> CFunction<Dom, Ran>::operator>(CFunction<Dom, Ran> const &rhs) const {
        std::string new_latex = this->_latex;
        new_latex.append(" > ");
        new_latex.append(rhs._latex);
        return CComparison<Dom>([lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) > rhs_f(z); },
                                     new_latex);
    }

    template<typename Dom, typename Ran>
    CComparison<Dom> CFunction<Dom, Ran>::operator<(CFunction<Dom, Ran> const &rhs) const {
        std::string new_latex = this->_latex;
        new_latex.append(" < ");
        new_latex.append(rhs._latex);
        return CComparison<Dom>([lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) < rhs_f(z); },
                                     new_latex);
    }

    template<typename Dom, typename Ran>
    CComparison<Dom> CFunction<Dom, Ran>::operator==(CFunction<Dom, Ran> const &rhs) const {
        std::string new_latex = this->_latex;
        new_latex.append(" \\eq ");
        new_latex.append(rhs._latex);
        return CComparison<Dom>([lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept {
            return Traits<Ran>::close(lhs_f(z), rhs_f(z));
        }, new_latex);
    }

    template<typename Dom, typename Ran>
    CComparison<Dom> CFunction<Dom, Ran>::operator>=(CFunction<Dom, Ran> const &rhs) const {
        std::string new_latex = this->_latex;
        new_latex.append(" \\ge ");
        new_latex.append(rhs._latex);
        return CComparison<Dom>([lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) >= rhs_f(z) || Traits<Ran>::close(lhs_f(z), rhs_f(z)); },
                                     new_latex);
    }

    template<typename Dom, typename Ran>
    CComparison<Dom> CFunction<Dom, Ran>::operator<=(CFunction<Dom, Ran> const &rhs) const {
        std::string new_latex = this->_latex;
        new_latex.append(" \\le ");
        new_latex.append(rhs._latex);
        return CComparison<Dom>([lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept { return lhs_f(z) <= rhs_f(z) || Traits<Ran>::close(lhs_f(z), rhs_f(z)); },
                                     new_latex);
    }

    template<typename Dom, typename Ran>
    CComparison<Dom> CFunction<Dom, Ran>::operator!=(CFunction<Dom, Ran> const &rhs) const {
        std::string new_latex = this->_latex;
        new_latex.append(" \\ne ");
        new_latex.append(rhs._latex);
        return CComparison<Dom>([lhs_f = this->_f, rhs_f = rhs._f](Dom const z) noexcept {
            return !Traits<Ran>::close(lhs_f(z), rhs_f(z));
        }, new_latex);
    }
}
