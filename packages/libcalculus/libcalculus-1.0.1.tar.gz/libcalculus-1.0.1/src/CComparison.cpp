#include "CComparison.h"

namespace libcalculus {
    template<typename Dom>
    CComparison<Dom> CComparison<Dom>::operator~() const {
        std::string new_latex = "\\neg\\left(";
        new_latex.append(this->latex);
        new_latex.append("\\right)");
        return CComparison([old_eval = this->eval](Dom z) { return !old_eval(z); }, new_latex);
    }

    template<typename Dom>
    CComparison<Dom> CComparison<Dom>::operator|(CComparison<Dom> const &rhs) const {
        std::string new_latex = "\\left(";
        new_latex.append(this->latex);
        new_latex.append("\\right)\\vee\\left(");
        new_latex.append(rhs.latex);
        new_latex.append("\\right)");
        return CComparison([lhs_eval = this->eval, rhs_eval = rhs.eval](Dom z) { return lhs_eval(z) || rhs_eval(z); },
                                     new_latex);
    }

    template<typename Dom>
    CComparison<Dom> CComparison<Dom>::operator&(CComparison<Dom> const &rhs) const {
        std::string new_latex = "\\left(";
        new_latex.append(this->latex);
        new_latex.append("\\right)\\wedge\\left(");
        new_latex.append(rhs.latex);
        new_latex.append("\\right)");
        return CComparison([lhs_eval = this->eval, rhs_eval = rhs.eval](Dom z) { return lhs_eval(z) && rhs_eval(z); },
                                     new_latex);
    }

    template<typename Dom>
    CComparison<Dom> &CComparison<Dom>::operator|=(CComparison<Dom> const &rhs) {
        std::string new_latex = "\\left(";
        new_latex.append(this->latex);
        new_latex.append("\\right)\\vee\\left(");
        new_latex.append(rhs.latex);
        new_latex.append("\\right)");
        this->eval = [lhs_eval = this->eval, rhs_eval = rhs.eval](Dom z) { return lhs_eval(z) || rhs_eval(z); };
        this->latex = new_latex;
        return *this;
    }

    template<typename Dom>
    CComparison<Dom> &CComparison<Dom>::operator&=(CComparison<Dom> const &rhs) {
        std::string new_latex = "\\left(";
        new_latex.append(this->latex);
        new_latex.append("\\right)\\wedge\\left(");
        new_latex.append(rhs.latex);
        new_latex.append("\\right)");
        this->eval = [lhs_eval = this->eval, rhs_eval = rhs.eval](Dom z) { return lhs_eval(z) && rhs_eval(z); };
        this->latex = new_latex;
        return *this;
    }
}
