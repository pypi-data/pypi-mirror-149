#pragma once
#include <string>
#include "Definitions.h"

namespace libcalculus {
    namespace Latex {
        std::string _parenthesize(std::string const &expr);
        std::string parenthesize_if(std::string const &expr, OP_TYPE const new_op, OP_TYPE const last_op);

        template<typename T> std::string fmt_const(T const a, bool const parenthesize = false);
    }
}
