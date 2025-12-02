# Building Your DSL

A guide to building your own DSL with Grammar School.

## Step 1: Define Your Methods

Methods are the functions that your DSL will support. They contain the actual implementation.

=== "Python"

    ```python
    from grammar_school import Grammar, method

    class MyDSL(Grammar):
        def __init__(self):
            super().__init__()
            self.users = []
            self.emails_sent = []

        @method
        def create_user(self, name, email):
            user = {"name": name, "email": email}
            self.users.append(user)
            print(f"Created user: {name}")

        @method
        def send_email(self, to, subject):
            email = {"to": to, "subject": subject}
            self.emails_sent.append(email)
            print(f"Sent email to {to}")
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

## Step 2: Use Your DSL

With the unified interface, methods execute directly - no Runtime needed!

=== "Python"

    ```python
    # Create your DSL instance
    dsl = MyDSL()

    # Execute DSL code - methods run directly
    dsl.execute('create_user(name="Alice", email="alice@example.com")')
    dsl.execute('send_email(to="bob@example.com", subject="Hello")')

    # Access state if needed
    print(f"Users: {dsl.users}")
    print(f"Emails sent: {dsl.emails_sent}")
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
    dsl = MyDSL()

    code = '''
    create_user(name="Alice", email="alice@example.com")
    send_email(to="alice@example.com", subject="Welcome!")
    '''

    dsl.execute(code)
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

1. **Keep Methods Simple** - Each method should do one thing
2. **Use Meaningful Method Names** - Make method names descriptive
3. **Handle Errors** - Validate inputs and handle errors appropriately
4. **Maintain State Carefully** - Use `self` attributes to manage state
5. **Document Your DSL** - Document what each method does

## Advanced: Method Chaining

Method chaining works naturally - methods can access state via `self`:

=== "Python"

    ```python
    class MusicDSL(Grammar):
        def __init__(self):
            super().__init__()
            self.tracks = []
            self.current_track = None

        @method
        def track(self, name):
            self.current_track = {"name": name, "clips": []}
            self.tracks.append(self.current_track)

        @method
        def add_clip(self, start, length):
            if self.current_track:
                self.current_track["clips"].append({
                    "start": start,
                    "length": length
                })
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
