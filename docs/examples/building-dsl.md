# Building Your DSL

A guide to building your own DSL with Grammar School.

## Step 1: Define Your Verbs

Verbs are the functions that your DSL will support.

=== "Python"

    ```python
    from grammar_school import Action, verb

    class MyDSL:
        @verb
        def create_user(self, name, email, _context=None):
            return Action(
                kind="create_user",
                payload={"name": name, "email": email}
            )

        @verb
        def send_email(self, to, subject, _context=None):
            return Action(
                kind="send_email",
                payload={"to": to, "subject": subject}
            )
    ```

=== "Go"

    ```go
    type MyDSL struct{}

    func (d *MyDSL) CreateUser(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
        name := args["name"].Str
        email := args["email"].Str
        action := gs.Action{
            Kind: "create_user",
            Payload: map[string]interface{}{
                "name":  name,
                "email": email,
            },
        }
        return []gs.Action{action}, ctx, nil
    }

    func (d *MyDSL) SendEmail(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
        to := args["to"].Str
        subject := args["subject"].Str
        action := gs.Action{
            Kind: "send_email",
            Payload: map[string]interface{}{
                "to":      to,
                "subject": subject,
            },
        }
        return []gs.Action{action}, ctx, nil
    }
    ```

## Step 2: Implement Your Runtime

The Runtime executes the Actions produced by your verbs.

=== "Python"

    ```python
    from grammar_school import Action, Runtime

    class MyRuntime(Runtime):
        def __init__(self):
            self.users = []
            self.emails_sent = []

        def execute(self, action: Action) -> None:
            if action.kind == "create_user":
                user = {
                    "name": action.payload["name"],
                    "email": action.payload["email"]
                }
                self.users.append(user)
                print(f"Created user: {user['name']}")

            elif action.kind == "send_email":
                email = {
                    "to": action.payload["to"],
                    "subject": action.payload["subject"]
                }
                self.emails_sent.append(email)
                print(f"Sent email to {email['to']}")
    ```

=== "Go"

    ```go
    type MyRuntime struct {
        users      []map[string]interface{}
        emailsSent []map[string]interface{}
    }

    func (r *MyRuntime) ExecuteAction(ctx context.Context, a gs.Action) error {
        switch a.Kind {
        case "create_user":
            user := map[string]interface{}{
                "name":  a.Payload["name"],
                "email": a.Payload["email"],
            }
            r.users = append(r.users, user)
            fmt.Printf("Created user: %v\n", user["name"])

        case "send_email":
            email := map[string]interface{}{
                "to":      a.Payload["to"],
                "subject": a.Payload["subject"],
            }
            r.emailsSent = append(r.emailsSent, email)
            fmt.Printf("Sent email to %v\n", email["to"])
        }
        return nil
    }
    ```

## Step 3: Use Your DSL

=== "Python"

    ```python
    from grammar_school import Grammar

    dsl = MyDSL()
    grammar = Grammar(dsl)
    runtime = MyRuntime()

    code = '''
    create_user(name="Alice", email="alice@example.com")
    send_email(to="alice@example.com", subject="Welcome!")
    '''

    grammar.execute(code, runtime)
    ```

=== "Go"

    ```go
    dsl := &MyDSL{}
    engine, _ := gs.NewEngine("", dsl, parser)
    runtime := &MyRuntime{}

    code := `
    create_user(name="Alice", email="alice@example.com")
    send_email(to="alice@example.com", subject="Welcome!")
    `

    plan, _ := engine.Compile(code)
    engine.Execute(context.Background(), runtime, plan)
    ```

## Best Practices

1. **Keep Verbs Simple** - Each verb should do one thing
2. **Use Meaningful Action Kinds** - Make action kinds descriptive
3. **Handle Errors** - Validate inputs and handle errors appropriately
4. **Maintain State Carefully** - Use the Runtime to manage state
5. **Document Your DSL** - Document what each verb does and what actions it produces

## Advanced: Method Chaining

You can support method chaining by returning context:

=== "Python"

    ```python
    @verb
    def track(self, name, _context=None):
        return Action(kind="create_track", payload={"name": name})

    @verb
    def add_clip(self, start, length, _context=None):
        # _context contains the previous action
        track_name = _context.payload["name"] if _context else None
        return Action(
            kind="add_clip",
            payload={"track": track_name, "start": start, "length": length}
        )
    ```

=== "Go"

    ```go
    func (d *MyDSL) Track(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
        name := args["name"].Str
        action := gs.Action{
            Kind: "create_track",
            Payload: map[string]interface{}{"name": name},
        }
        newCtx := gs.NewContext()
        newCtx.Set("track_name", name)
        return []gs.Action{action}, newCtx, nil
    }

    func (d *MyDSL) AddClip(args gs.Args, ctx *gs.Context) ([]gs.Action, *gs.Context, error) {
        trackName, _ := ctx.Get("track_name")
        action := gs.Action{
            Kind: "add_clip",
            Payload: map[string]interface{}{
                "track":  trackName,
                "start":  args["start"].Num,
                "length": args["length"].Num,
            },
        }
        return []gs.Action{action}, ctx, nil
    }
    ```
