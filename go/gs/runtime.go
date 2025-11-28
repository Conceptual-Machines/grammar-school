package gs

import "context"

// Runtime is the interface for runtime implementations that execute actions.
type Runtime interface {
	ExecuteAction(ctx context.Context, a Action) error
}

