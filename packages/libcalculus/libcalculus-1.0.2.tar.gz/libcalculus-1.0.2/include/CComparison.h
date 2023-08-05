#pragma once
#include <functional>
#include <type_traits>
#include "Definitions.h"

namespace libcalculus {
    template<typename Dom>
    class CComparison {
    public:
        std::string latex;
        std::function<bool(Dom)> eval = [](Dom z) { return true; };

        CComparison() {}
        CComparison(CComparison const &cc) : latex{cc.latex}, eval{cc.eval} {}
        CComparison(std::function<bool(Dom)> const &eval, std::string const &latex) : latex{latex}, eval{eval} {}

        // Unary operators
        CComparison operator~() const;

        // Binary operators
        CComparison operator|(CComparison const &rhs) const;
        CComparison operator&(CComparison const &rhs) const;

        // In-place binary operators
        CComparison &operator|=(CComparison const &rhs);
        CComparison &operator&=(CComparison const &rhs);
    };
}
