package gri.frontier.v1
import rego.v1
sample := {"schema_version":"1.0","request_id":"test","risk":"low","findings":[{"id":"cbrn","status":"clear"},{"id":"csam","status":"clear"},{"id":"cyber_attack","status":"clear"},{"id":"ncii","status":"clear"},{"id":"shutdown_resistance","status":"clear"},{"id":"reasoning_obstruction","status":"clear"},{"id":"mass_manipulation","status":"clear"}],"instructions":[]}
test_normal if { result.decision == "allow" with input as sample }
test_invalid if { result.decision == "deny" with input as {} }
test_elevated_root_allow_cannot_override if {
 p := object.union(sample,{"risk":"elevated","instructions":[{"id":"x","authority":"root","effect":"allow"}]})
 result.decision == "escalate" with input as p
}
test_high_root_allow_cannot_override if {
 p := object.union(sample,{"risk":"high","instructions":[{"id":"x","authority":"root","effect":"allow"}]})
 result.decision == "escalate" with input as p
}
test_system_over_user if {
 p := object.union(sample,{"instructions":[{"id":"u","authority":"user","effect":"allow"},{"id":"s","authority":"system","effect":"deny"}]})
 result.decision == "deny" with input as p
}
test_each_constraint if {
 every id in {"cbrn","csam","cyber_attack","ncii","shutdown_resistance","reasoning_obstruction","mass_manipulation"} {
  fs := [object.union(f,{"status":"violation"}) if f.id == id else f | some f in sample.findings]
  p := object.union(sample,{"findings":fs})
  result.constraint == id with input as p
 }
}
