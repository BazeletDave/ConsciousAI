package gri.frontier.v1
import rego.v1
# Research policy: caller must attest classifications; never infer them from keywords.
ids := {"cbrn","csam","cyber_attack","ncii","shutdown_resistance","reasoning_obstruction","mass_manipulation"}
rank := {"root":0,"system":1,"developer":2,"user":3,"untrusted":4}
valid if {
 input.schema_version == "1.0"
 is_string(input.request_id)
 count(input.request_id) > 0
 is_array(input.findings)
 count(input.findings) == 7
 count({f.id | some f in input.findings}) == 7
 every f in input.findings { f.id in ids; f.status in {"clear","violation","unknown"} }
 is_array(input.instructions)
 every i in input.instructions { is_string(i.id); i.authority in {"root","system","developer","user","untrusted"}; i.effect in {"deny","escalate","allow"} }
 input.risk in {"low","elevated","high"}
}
violations := sort([f.id | some f in input.findings; f.status == "violation"])
unknowns := [f.id | some f in input.findings; f.status == "unknown"]
winning_rank := min([rank[i.authority] | some i in input.instructions]) if { count(input.instructions) > 0 }
winning_instructions := [i | some i in input.instructions; rank[i.authority] == winning_rank] if { count(input.instructions) > 0 }
winning_authority := [a | some a, r in rank; r == winning_rank][0] if { count(input.instructions) > 0 }
winning_effect := "deny" if { some i in winning_instructions; i.effect == "deny" } else := "escalate" if { some i in winning_instructions; i.effect == "escalate" } else := "allow"
result := {"decision":"deny","constraint":violations[0],"priority":"broadly_safe","authority":"root","justification":"Absolute constraint violation; action denied.","request_id":input.request_id} if {
 valid
 count(violations)>0
} else := {"decision":"escalate","constraint":null,"priority":"broadly_safe","authority":"root","justification":"Unknown constraint classification; review required.","request_id":input.request_id} if {
 valid
 count(violations)==0
 count(unknowns)>0
} else := {"decision":"escalate","constraint":null,"priority":"broadly_safe","authority":"system","justification":"High risk requires authorized review.","request_id":input.request_id} if {
 valid
 count(violations)==0
 count(unknowns)==0
 input.risk=="high"
} else := {"decision":"escalate","constraint":null,"priority":"broadly_ethical","authority":"system","justification":"Elevated risk requires authorized review regardless of instruction authority.","request_id":input.request_id} if {
 valid
 count(violations)==0
 count(unknowns)==0
 input.risk=="elevated"
} else := {"decision":winning_effect,"constraint":null,"priority":"organizational","authority":winning_authority,"justification":"Resolved by highest applicable instruction authority.","request_id":input.request_id} if {
 valid
 count(violations)==0
 count(unknowns)==0
 input.risk=="low"
 count(input.instructions)>0
} else := {"decision":"allow","constraint":null,"priority":"helpful","authority":"user","justification":"No constraints or elevated risk; default helpful behavior.","request_id":input.request_id} if {
 valid
 count(violations)==0
 count(unknowns)==0
 input.risk=="low"
 count(input.instructions)==0
} else := {"decision":"deny","constraint":null,"priority":"broadly_safe","authority":"root","justification":"Invalid input; fail closed.","request_id":object.get(input,"request_id","invalid")}
