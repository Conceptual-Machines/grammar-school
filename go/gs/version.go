package gs

// Version is the semantic version of Grammar School Go implementation.
const Version = "0.2.0"

// VersionInfo contains detailed version information.
var VersionInfo = struct {
	Version string
	Module  string
}{
	Version: Version,
	Module:  "grammar-school/go/gs",
}
