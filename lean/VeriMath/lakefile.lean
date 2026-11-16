import Lake
open Lake DSL

package VeriMath where
  name := "VeriMath"
  version := "1.0.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "stable"

lean_lib VeriMath where
  roots := #[`VeriMath.Tactics]
