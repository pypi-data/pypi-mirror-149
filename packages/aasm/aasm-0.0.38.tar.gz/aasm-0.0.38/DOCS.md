# Agents Assembly instructions

## Type annotation definitions

`{...}` - one of the options from the brackets needs to be chosen, written as specified within brackets

`Name` - A unique within alphanumeric string, which does not contain any forbidden characters and does not begin with a numberA unique within alphanumeric string, which does not contain any forbidden characters and does not begin with a number. Some instructions put further restrictions on `Name`s. Some instructions put further restrictions on `Name`s.

`Float` - A floating point number or variable

`MutFloat` - A floating point variable with possibility of modification

`Integer` - An integer. If a `Float` is passed as an argument of this type it will be rounded down.

`Enum` - An enumerable, stores a state in the form of `EnumVal`

`EnumVal` - A distinct enumerable state

`Message` - A message defined using the `MESSAGE` instruction

`Jid` - Systemic agent identifier

`ACLPerformative` - One of FIPA defined ACL performative types.

`DistArgs` - Arguments for a specified distribution. Mathematical constraints apply.


## Scope Modifiers

`GRAPH` | **args:** `type: {statistical}` | Enters the scope for creation of a graph of specified `type`

`EGRAPH` | - | Exists graph scope. Has to correspond to `GRAPH`

*Example usage:*
```aasm
GRAPH statistical
#
# graph definition here
#
EGRAPH
```

`ACTION` | **args:** `name: Name, type: {modify_self, send_msg}` | Enters scope for describing an Action of the specified `type`. The name is required to be unique within `BEHAV` scope. It can only be used within `BEHAV` scope.

`EACTION` | - | Exists action scope. Has to correspond to `ACTION`

*Example usage:*
```aasm
ACTION add_friend, modify_self
#
# action definition here
#
EACTION
```

`BEHAV` | **args:** `name: Name, type: {setup, one_time, cyclic, msg_rcv}, b_args<sup>**</sup>` | Enters scope for describing a Behaviour of specified `type`. `b_args` depend on the specified `type`. The name is required to be unique within `AGENT` scope. It can only be used within `AGENT` scope.

`b_args:`
 * `setup`: | - | Fires on setup
 * `one_time`: | `delay: Float` | Fires after `delay` seconds. `delay` must be greater than `0`.
 * `cyclic`: | `cycle: Float` | Fires every `cycle` seconds. `cycle` must be greater than `0`.
 * `msg_rcv`: | `msg_name: Name, msg_type: ACLPerformative` | Fires upon receiving message matching name `msg_name` and `msg_type`.

`EBEHAV` | - | Exists behaviour scope. Has to correspond to `BEHAV`

*Example usage:*
```aasm
BEHAV read_message, msg_rcv, test_message, inform
#
# behaviour definition here
#
EBEHAV
```

`MESSAGE` | **args:** `name: Name, performative: ACLPerformative` | Enters the scope for describing a Message of specified name and performative

`EMESSAGE` | - | Exists message scope. Has to correspond to `MESSAGE`.

*Example usage:*
```aasm
MESSAGE test_message, inform
#
# message definitnion here
#
EMESSAGE
```

`AGENT` | **args:** `name: Name` | Enters the scope for describing an agent.

`EAGENT` | - | Exists agent scope. Has to correspond to `AGENT`

*Example usage*
```aasm
AGENT
#
# agent definition here
#
EAGENT
```

## Message Scope
`PRM` | **args:** `name: Name, type: {float}` | Creates a new message parameter of specified type. `name` cannot be `sender`, `type`, `performative`.

## Agent Scope
`PRM` | **args:** `name: Name, type: {float, enum, list}, subtype: {init, dist, conn, msg}, p_args<sup>**</sup>` | Creates an agent parameter of specified type and subtype. Describes the initial state of an agent by passing arguments `p_args`.

`p_args:`
 * `float`
   * `init`: | `val: Float` | Creates a float parameter. Value `name` is set to `val` during agent initiation.
   * `dist`: | `dist: {normal, uniform, exp}, dist_args: DistArgs}` | Creates a float parameter. Value `name` is set to a value drawn from specified `dist` distribution.
 * `enum`: | `[val1, val1%, ..., valn, valn%]` | Creates an enum parameter. Value `name` is set to one of `[val1,...,val n]`. Corresponding `valn%` arguments specify the percentage of the total agent population to have a specific value set on startup.
 * `list`
   * `conn`: | - | Creates a connection list parameter. List is empty on startup.
   * `msg`: | - | Creates a message list parameter. List is empty on startup.

## Action Scope: modifiers

`DECL` | **args:** `name: Name, value: Float` | Creates a float variable with name and value. The new variable can only be used in given action's scope.

`SET` | **args:** `dst: MutFloat/Enum, value: Float/EnumVal` | Sets value of `dst` to `value`

`SUBS` | **args:** `dst: List, src: List, num: Integer` | Chooses `num` elements from `src` and sets `dst` to them.

## Action Scope: math expressions

`ADD` | **args:** `dst: MutFlost, arg: Float` | Adds `arg` to `dst` and stores result in `dst`.

`MULT` | **args:** `dst: MutFlost, arg: Float` | Multiplies `arg` by `dst` and stores result in `dst`.

`SUBT` | **args:** `dst: MutFlost, arg: Float` | Subtracts `arg` from `dst` and stores result in `dst`.

`DIV` | **args:** `dst: MutFlost, arg: Float` | Divides `arg` by `dst` and stores result in `dst`. If `arg` is `0` then the `ACTION` will finish early.

## Action Scope: conditionals
`IEQ` | **args** `a: Float/Enum, b: Float/EnumVal` | Begins conditional block if `a` is equal to `b`. Needs matching `EBLOCK`.

`INEQ` | **args** `a: Float/Enum, b: Float/EnumVal` | Begins conditional block if `a` is not equal to `b`. Needs matching `EBLOCK`.

`ILT` | **args** `a: Float, b: Float` | Begins conditional block if `a` is less than `b`. Needs matching `EBLOCK`.

`IGT` | **args** `a: Float, b: Float` | Begins conditional block if `a` is greater than `b`. Needs matching `EBLOCK`.

`ILTEQ` | **args** `a: Float, b: Float` | Begins conditional block if `a` is less or equal`b`. Needs matching `EBLOCK`.

`IGTEQ` | **args** `a: Float, b: Float` | Begins conditional block if `a` is greater or equal`b`. Needs matching `EBLOCK`.

## Action Scope: loops
`WEQ` | **args** `a: Float/Enum, b: Float/EnumVal` | Begins loop block if `a` is equal to `b`. Needs matching `EBLOCK`.

`WNEQ` | **args** `a: Float/Enum, b: Float/EnumVal` | Begins loop block if `a` is not equal to `b`. Needs matching `EBLOCK`.

`WLT` | **args** `a: Float, b: Float` | Begins loop block if `a` is less than `b`. Needs matching `EBLOCK`.

`WGT` | **args** `a: Float, b: Float` | Begins loop block if `a` is greater than `b`. Needs matching `EBLOCK`.

`WLTEQ` | **args** `a: Float, b: Float` | Begins loop block if `a` is less or equal`b`. Needs matching `EBLOCK`.

`WGTEQ` | **args** `a: Float, b: Float` | Begins loop block if `a` is greater or equal`b`. Needs matching `EBLOCK`.

## Action scope: lists

`ADDE` | **args:** `list: List, value: Message/Jid` | Adds `value` to `list`.

`REME` | **args:** `list: List, value: Message/Jid` | Removes `value` from `list`. If `value` is not in the list, does nothing.

`REMEN` | **args:** `list: List, num, Integer` | Removes `num` random elements from `list`. If `list` is too short, it clears it.

`LEN` | **args:** `result: MutFlost, list: List` | Saves length of `list` in `result`.

`CLR` | **args:** `list: List` | Clears contents of `list`

`IN` | **args:** `list: List, value: Message/Jid` | Begins conditional block if `val` is in `list`. Needs matching `EBLOCK`

`NIN` | **args:** `list: List, value: Message/Jid` | Begins conditional block if `val` is not in `list`. Needs matching `EBLOCK`

## Action scope: special

`EBLOCK` | - | Ends current conditional or loop block.

`SEND` | **args:** `rcv: ConnList/Jid` | Sends message to `rcv`. Can only be used inside `send_msg` actions.

`RAND` | **args:** `result: MutFloat, cast: {float, int}, dist: {uniform, normal, exp}, dist_args: DistArgs` | Stores a value drawn from specified `dist` distribution, casts it to `cast` type and stores it in `result`

`(Message Access)` | **usage:** `[MSG].[prm]` | Allows to access the value of `prm` from `MSG`
