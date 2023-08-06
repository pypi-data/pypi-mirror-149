"""Amalgamation of xonsh.prompt package, made up of the following modules, in order:

* base
* cwd
* env
* job
* times
* vc

"""

from sys import modules as _modules
from types import ModuleType as _ModuleType
from importlib import import_module as _import_module


class _LazyModule(_ModuleType):

    def __init__(self, pkg, mod, asname=None):
        '''Lazy module 'pkg.mod' in package 'pkg'.'''
        self.__dct__ = {
            'loaded': False,
            'pkg': pkg,  # pkg
            'mod': mod,  # pkg.mod
            'asname': asname,  # alias
            }

    @classmethod
    def load(cls, pkg, mod, asname=None):
        if mod in _modules:
            key = pkg if asname is None else mod
            return _modules[key]
        else:
            return cls(pkg, mod, asname)

    def __getattribute__(self, name):
        if name == '__dct__':
            return super(_LazyModule, self).__getattribute__(name)
        dct = self.__dct__
        mod = dct['mod']
        if dct['loaded']:
            m = _modules[mod]
        else:
            m = _import_module(mod)
            glbs = globals()
            pkg = dct['pkg']
            asname = dct['asname']
            if asname is None:
                glbs[pkg] = m = _modules[pkg]
            else:
                glbs[asname] = m
            dct['loaded'] = True
        return getattr(m, name)

#
# base
#
"""Base prompt, provides PROMPT_FIELDS and prompt related functions"""

itertools = _LazyModule.load('itertools', 'itertools')
os = _LazyModule.load('os', 'os')
re = _LazyModule.load('re', 're')
socket = _LazyModule.load('socket', 'socket')
sys = _LazyModule.load('sys', 'sys')
tp = _LazyModule.load('typing', 'typing', 'tp')
xp = _LazyModule.load('xonsh', 'xonsh.platform', 'xp')
xt = _LazyModule.load('xonsh', 'xonsh.tools', 'xt')
from xonsh.built_ins import XSH

if tp.TYPE_CHECKING:
    from xonsh.built_ins import XonshSession

    FieldType = tp.TypeVar("FieldType", bound="BasePromptField", covariant=True)


@xt.lazyobject
def DEFAULT_PROMPT():
    return default_prompt()


class _ParsedToken(tp.NamedTuple):
    """It can either be a literal value alone or a field and its resultant value"""

    value: str
    field: tp.Optional[str] = None


class ParsedTokens(tp.NamedTuple):
    tokens: tp.List[_ParsedToken]
    template: tp.Union[str, tp.Callable]

    def process(self) -> str:
        """Wrapper that gets formatter-function from environment and returns final prompt."""
        processor = XSH.env.get(  # type: ignore
            "PROMPT_TOKENS_FORMATTER", prompt_tokens_formatter_default
        )
        return processor(self)

    def update(
        self,
        idx: int,
        val: tp.Optional[str],
        spec: tp.Optional[str],
        conv: tp.Optional[str],
    ) -> None:
        """Update tokens list in-place"""
        if idx < len(self.tokens):
            tok = self.tokens[idx]
            self.tokens[idx] = _ParsedToken(_format_value(val, spec, conv), tok.field)


def prompt_tokens_formatter_default(container: ParsedTokens) -> str:
    """
        Join the tokens

    Parameters
    ----------
    container: ParsedTokens
        parsed tokens holder

    Returns
    -------
    str
        process the tokens and finally return the prompt string
    """
    return "".join([tok.value for tok in container.tokens])


class PromptFormatter:
    """Class that holds all the related prompt formatting methods,
    uses the ``PROMPT_FIELDS`` envvar (no color formatting).
    """

    def __call__(self, template=DEFAULT_PROMPT, fields=None, **kwargs) -> str:
        """Formats a xonsh prompt template string."""

        if fields is None:
            self.fields = XSH.env["PROMPT_FIELDS"]  # type: ignore
        else:
            self.fields = fields

        # some quick tests
        if isinstance(fields, dict):
            pflds: "PromptFields[PromptField]" = PromptFields(XSH, init=False)
            pflds.update(fields)
            self.fields = pflds

        try:
            toks = self._format_prompt(template=template, **kwargs)
            prompt = toks.process()
        except Exception as ex:
            # make it obvious why it has failed
            import logging

            logging.error(str(ex), exc_info=True)
            xt.print_exception(
                f"Failed to format prompt `{template}`-> {type(ex)}:{ex}"
            )
            return _failover_template_format(template)
        return prompt

    def _format_prompt(self, template=DEFAULT_PROMPT, **kwargs) -> ParsedTokens:
        tmpl = template() if callable(template) else template
        toks = []
        for literal, field, spec, conv in xt.FORMATTER.parse(tmpl):
            if literal:
                toks.append(_ParsedToken(literal))
            entry = self._format_field(field, spec, conv, idx=len(toks), **kwargs)
            if entry is not None:
                toks.append(_ParsedToken(entry, field))

        return ParsedTokens(toks, template)

    def _format_field(self, field, spec="", conv=None, **kwargs):
        if field is None:
            return
        elif field.startswith("$"):
            val = XSH.env[field[1:]]
            return _format_value(val, spec, conv)
        elif field in self.fields:
            val = self._get_field_value(field, spec=spec, conv=conv, **kwargs)
            return _format_value(val, spec, conv)
        else:
            # color or unknown field, return as is
            return "{" + field + "}"

    def _get_field_value(self, field, **_):
        try:
            return self.fields.pick(field)
        except Exception:  # noqa
            print("prompt: error: on field {!r}" "".format(field), file=sys.stderr)
            xt.print_exception()
            value = f"{{BACKGROUND_RED}}{{ERROR:{field}}}{{RESET}}"
        return value


def default_prompt():
    """Creates a new instance of the default prompt."""
    if xp.ON_CYGWIN or xp.ON_MSYS:
        dp = (
            "{env_name}"
            "{BOLD_GREEN}{user}@{hostname}"
            "{BOLD_BLUE} {cwd} {prompt_end}{RESET} "
        )
    elif xp.ON_WINDOWS and not xp.win_ansi_support():
        dp = (
            "{env_name}"
            "{BOLD_INTENSE_GREEN}{user}@{hostname}{BOLD_INTENSE_CYAN} "
            "{cwd}{branch_color}{curr_branch: {}}{RESET} "
            "{BOLD_INTENSE_CYAN}{prompt_end}{RESET} "
        )
    else:
        dp = (
            "{env_name}"
            "{BOLD_GREEN}{user}@{hostname}{BOLD_BLUE} "
            "{cwd}{branch_color}{curr_branch: {}}{RESET} "
            "{BOLD_BLUE}{prompt_end}{RESET} "
        )
    return dp


def _failover_template_format(template):
    if callable(template):
        try:
            # Exceptions raises from function of producing $PROMPT
            # in user's xonshrc should not crash xonsh
            return template()
        except Exception:
            xt.print_exception()
            return "$ "
    return template


@xt.lazyobject
def RE_HIDDEN():
    return re.compile("\001.*?\002")


def multiline_prompt(curr=""):
    """Returns the filler text for the prompt in multiline scenarios."""
    line = curr.rsplit("\n", 1)[1] if "\n" in curr else curr
    line = RE_HIDDEN.sub("", line)  # gets rid of colors
    # most prompts end in whitespace, head is the part before that.
    head = line.rstrip()
    headlen = len(head)
    # tail is the trailing whitespace
    tail = line if headlen == 0 else line.rsplit(head[-1], 1)[1]
    # now to construct the actual string
    dots = XSH.env.get("MULTILINE_PROMPT")
    dots = dots() if callable(dots) else dots
    if dots is None or len(dots) == 0:
        return ""
    tokstr = xt.format_color(dots, hide=True)
    baselen = 0
    basetoks = []
    for x in tokstr.split("\001"):
        pre, sep, post = x.partition("\002")
        if len(sep) == 0:
            basetoks.append(("", pre))
            baselen += len(pre)
        else:
            basetoks.append(("\001" + pre + "\002", post))
            baselen += len(post)
    if baselen == 0:
        return xt.format_color("{RESET}" + tail, hide=True)
    toks = basetoks * (headlen // baselen)
    n = headlen % baselen
    count = 0
    for tok in basetoks:
        slen = len(tok[1])
        newcount = slen + count
        if slen == 0:
            continue
        elif newcount <= n:
            toks.append(tok)
        else:
            toks.append((tok[0], tok[1][: n - count]))
        count = newcount
        if n <= count:
            break
    toks.append((xt.format_color("{RESET}", hide=True), tail))
    rtn = "".join(itertools.chain.from_iterable(toks))
    return rtn


def is_template_string(template, PROMPT_FIELDS=None):
    """Returns whether or not the string is a valid template."""
    template = template() if callable(template) else template
    try:
        included_names = {i[1] for i in xt.FORMATTER.parse(template)}
    except ValueError:
        return False
    included_names.discard(None)
    if PROMPT_FIELDS is None:
        fmtter = XSH.env.get("PROMPT_FIELDS", PROMPT_FIELDS)
    else:
        fmtter = PROMPT_FIELDS
    known_names = set(fmtter.keys())
    return included_names <= known_names


def _format_value(val, spec, conv) -> str:
    """Formats a value from a template string {val!conv:spec}. The spec is
    applied as a format string itself, but if the value is None, the result
    will be empty. The purpose of this is to allow optional parts in a
    prompt string. For example, if the prompt contains '{current_job:{} | }',
    and 'current_job' returns 'sleep', the result is 'sleep | ', and if
    'current_job' returns None, the result is ''.
    """
    if val is None:
        return ""
    val = xt.FORMATTER.convert_field(val, conv)

    if spec:
        val = xt.FORMATTER.format(spec, val)
    if not isinstance(val, str):
        val = format(val)
    return val


class PromptFields(tp.MutableMapping[str, "FieldType"]):
    """Mapping of functions available for prompt-display."""

    def __init__(self, xsh: "XonshSession", init=True):
        self._items: "dict[str, str | tp.Callable[..., str]]" = {}

        self._cache: "dict[str, str|FieldType]" = {}
        """for callbacks this will catch the value and should be cleared between prompts"""

        self.xsh = xsh
        if init:
            self.load_initial()

    def __repr__(self):
        return f"{self.__class__.__module__}.{self.__class__.__name__}(...)"

    def _repr_pretty_(self, p, cycle):
        name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        with p.group(1, name + "(", ")"):
            if cycle:
                p.text("...")
            elif len(self):
                p.break_()
                p.pretty(dict(self))

    def __getitem__(self, item: "str|BasePromptField"):
        # todo: load on-demand from modules
        if isinstance(item, BasePromptField):
            item = item.name
        return self._items[item]

    def __delitem__(self, key):
        del self._items[key]

    def __iter__(self):
        yield from self._items

    def __len__(self):
        return len(self._items)

    def __setitem__(self, key, value):
        self._items[key] = value

    def get_fields(self, module):
        """Find and load all instances of PromptField from the given module.

        Each module is expected to have a single prompt-field with the same name as the module
        """
        mod_name = module.__name__.replace(module.__package__, "", 1).replace(
            ".", "", 1
        )
        for attr, val in vars(module).items():
            if isinstance(val, BasePromptField):
                if attr == mod_name:
                    name = attr
                else:
                    name = f"{mod_name}.{attr}"
                val.name = name
                yield val

    def load_initial(self):
        from xonsh.prompt import gitstatus
        from xonsh.prompt.cwd import (
            _collapsed_pwd,
            _dynamically_collapsed_pwd,
            _replace_home_cwd,
        )
        from xonsh.prompt.env import env_name, vte_new_tab_cwd
        from xonsh.prompt.job import _current_job
        from xonsh.prompt.times import _localtime
        from xonsh.prompt.vc import branch_bg_color, branch_color, current_branch

        self.update(
            dict(
                user=xp.os_environ.get(
                    "USERNAME" if xp.ON_WINDOWS else "USER", "<user>"
                ),
                prompt_end="#" if xt.is_superuser() else "$",
                hostname=socket.gethostname().split(".", 1)[0],
                cwd=_dynamically_collapsed_pwd,
                cwd_dir=lambda: os.path.join(os.path.dirname(_replace_home_cwd()), ""),
                cwd_base=lambda: os.path.basename(_replace_home_cwd()),
                short_cwd=_collapsed_pwd,
                curr_branch=current_branch,
                branch_color=branch_color,
                branch_bg_color=branch_bg_color,
                current_job=_current_job,
                env_name=env_name,
                env_prefix="(",
                env_postfix=") ",
                vte_new_tab_cwd=vte_new_tab_cwd,
                time_format="%H:%M:%S",
                localtime=_localtime,
            )
        )
        for val in self.get_fields(gitstatus):
            self[val.name] = val

    def pick(self, key: "str|FieldType") -> "str | FieldType | None":
        """Get the value of the prompt-field

        Notes
        -----
            If it is callable, then the result of the callable is returned.
            If it is a PromptField then it is updated
        """
        name = key if isinstance(key, str) else key.name
        if name not in self._items:
            return None
        value = self._items[name]
        if name not in self._cache:
            if isinstance(value, BasePromptField):
                value.update(self)
            elif callable(value):
                value = value()

            # store in cache
            self._cache[name] = value
        return self._cache[name]

    def pick_val(self, key):
        """wrap .pick() method to get .value attribute in case of PromptField"""
        val = self.pick(key)
        return val.value if isinstance(val, BasePromptField) else val

    def needs_calling(self, name) -> bool:
        """check if we can offload the work"""
        if name in self._cache or (name not in self._items):
            return False

        value = self[name]
        return isinstance(value, BasePromptField) or callable(value)

    def reset(self):
        """the results are cached and need to be reset between prompts"""
        self._cache.clear()


class BasePromptField:
    value = ""
    """This field should hold the bare value of the field without any color/format strings"""

    _name: "str|None" = None
    updator: "tp.Callable[[FieldType, PromptFields], None] | None" = None
    """this is a callable that needs to update the value or any of the attribute of the field"""

    def __init__(
        self,
        **kwargs,
    ):
        """

        Parameters
        ----------
        kwargs
            attributes of the class will be set from this
        """

        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def update(self, ctx: PromptFields) -> None:
        """will be called from PromptFields getter for each new prompt"""
        if self.updator:
            self.updator(self, ctx)

    def __format__(self, format_spec: str):
        return format(self.value, format_spec)

    def __bool__(self):
        return bool(self.value)

    def __repr__(self):
        return f"<Prompt: {self._name}>"

    @classmethod
    def wrap(cls, **kwargs) -> "tp.Callable[..., FieldType]":
        """decorator to set the updator"""

        def wrapped(func):
            return cls(updator=func, **kwargs)

        return wrapped

    @property
    def name(self) -> str:
        """will be set during load.

        Notes
        -----
            fields with names such as ``gitstatus.branch`` mean they are defined in a module named ``gitstatus`` and
            are most likely a subfield used by ``gitstatus``
        """

        if self._name is None:
            raise NotImplementedError("PromptField name is not set")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value


class PromptField(BasePromptField):
    """Any new non-private attributes set by the sub-classes are considered a way to configure the format"""

    # these three fields will get updated by the caller
    prefix = ""
    suffix = ""

    def __format__(self, format_spec: str):
        if self.value:
            return self.prefix + format(self.value, format_spec) + self.suffix
        return ""


class MultiPromptField(BasePromptField):
    """Facilitate combining other PromptFields"""

    separator = ""
    """in case this combines values from other prompt fields"""

    fragments: "tuple[str, ...]" = ()
    """name of the fields or the literals to combine.
    If the framgment name startswith ``.`` then they are resolved to include the name of this field."""

    def __init__(self, *fragments: "str", **kwargs):
        super().__init__(**kwargs)
        self.fragments = fragments or self.fragments

    def get_frags(self, env):
        yield from self.fragments

    def _collect(self, ctx):
        for frag in self.get_frags(ctx.xsh.env):
            if frag.startswith("."):
                field_name = f"{self.name}{frag}"
                if field_name in ctx:
                    frag = field_name

            if frag in ctx:
                yield format(ctx.pick(frag))
            elif isinstance(frag, str):
                yield frag

    def update(self, ctx: PromptFields):
        self.value = self.separator.join(self._collect(ctx))

#
# cwd
#
"""CWD related prompt formatter"""

# amalgamated os
shutil = _LazyModule.load('shutil', 'shutil')
# amalgamated xonsh.platform
# amalgamated xonsh.tools
# amalgamated from xonsh.built_ins import XSH
def _replace_home(x: str):
    home = os.path.expanduser("~")
    if x.startswith(home):
        x = x.replace(home, "~", 1)

    if xp.ON_WINDOWS:
        if XSH.env.get("FORCE_POSIX_PATHS") and os.altsep:
            x = x.replace(os.sep, os.altsep)

    return x


def _replace_home_cwd():
    pwd = XSH.env["PWD"].replace("{", "{{").replace("}", "}}")
    return _replace_home(pwd)


def _collapsed_pwd():
    sep = xt.get_sep()
    pwd = _replace_home_cwd().split(sep)
    size = len(pwd)
    leader = sep if size > 0 and len(pwd[0]) == 0 else ""
    base = [
        i[0] if ix != size - 1 and i[0] != "." else i[0:2] if ix != size - 1 else i
        for ix, i in enumerate(pwd)
        if len(i) > 0
    ]
    return leader + sep.join(base)


def _dynamically_collapsed_pwd():
    """Return the compact current working directory.  It respects the
    environment variable DYNAMIC_CWD_WIDTH.
    """
    original_path = _replace_home_cwd()
    target_width, units = XSH.env["DYNAMIC_CWD_WIDTH"]
    elision_char = XSH.env["DYNAMIC_CWD_ELISION_CHAR"]
    if target_width == float("inf"):
        return original_path
    if units == "%":
        cols, _ = shutil.get_terminal_size()
        target_width = (cols * target_width) // 100
    sep = xt.get_sep()
    pwd = original_path.split(sep)
    last = pwd.pop()
    remaining_space = target_width - len(last)
    # Reserve space for separators
    remaining_space_for_text = remaining_space - len(pwd)
    parts = []
    for i in range(len(pwd)):
        part = pwd[i]
        part_len = int(
            min(len(part), max(1, remaining_space_for_text // (len(pwd) - i)))
        )
        remaining_space_for_text -= part_len
        if len(part) > part_len:
            reduced_part = part[0 : part_len - len(elision_char)] + elision_char
            parts.append(reduced_part)
        else:
            parts.append(part)
    parts.append(last)
    full = sep.join(parts)
    truncature_char = elision_char if elision_char else "..."
    # If even if displaying one letter per dir we are too long
    if len(full) > target_width:
        # We truncate the left most part
        full = truncature_char + full[int(-target_width) + len(truncature_char) :]
        # if there is not even a single separator we still
        # want to display at least the beginning of the directory
        if full.find(sep) == -1:
            full = (truncature_char + sep + last)[
                0 : int(target_width) - len(truncature_char)
            ] + truncature_char
    return full

#
# env
#
"""Prompt formatter for virtualenv and others"""
functools = _LazyModule.load('functools', 'functools')
# amalgamated re
from pathlib import Path
from typing import Optional

# amalgamated from xonsh.built_ins import XSH
def find_env_name() -> Optional[str]:
    """Find current environment name from available sources.

    If ``$VIRTUAL_ENV`` is set, it is determined from the prompt setting in
    ``<venv>/pyvenv.cfg`` or from the folder name of the environment.

    Otherwise - if it is set - from ``$CONDA_DEFAULT_ENV``.
    """
    virtual_env = XSH.env.get("VIRTUAL_ENV")
    if virtual_env:
        name = _determine_env_name(virtual_env)
        if name:
            return name
    conda_default_env = XSH.env.get("CONDA_DEFAULT_ENV")
    if conda_default_env:
        return conda_default_env


def env_name() -> str:
    """Build env_name based on different sources. Respect order of precedence.

    Name from VIRTUAL_ENV_PROMPT will be used as-is.
    Names from other sources are surrounded with ``{env_prefix}`` and
    ``{env_postfix}`` fields.
    """
    if XSH.env.get("VIRTUAL_ENV_DISABLE_PROMPT"):
        return ""
    virtual_env_prompt = XSH.env.get("VIRTUAL_ENV_PROMPT")
    if virtual_env_prompt:
        return virtual_env_prompt
    found_envname = find_env_name()
    return _surround_env_name(found_envname) if found_envname else ""


@functools.lru_cache(maxsize=5)
def _determine_env_name(virtual_env: str) -> str:
    """Use prompt setting from pyvenv.cfg or basename of virtual_env.

    Tries to be resilient to subtle changes in whitespace and quoting in the
    configuration file format as it adheres to no clear standard.
    """
    venv_path = Path(virtual_env)
    pyvenv_cfg = venv_path / "pyvenv.cfg"
    if pyvenv_cfg.is_file():
        match = re.search(r"prompt\s*=\s*(.*)", pyvenv_cfg.read_text())
        if match:
            return match.group(1).strip().lstrip("'\"").rstrip("'\"")
    return venv_path.name


def _surround_env_name(name: str) -> str:
    pf = XSH.shell.prompt_formatter
    pre = pf._get_field_value("env_prefix")
    post = pf._get_field_value("env_postfix")
    return f"{pre}{name}{post}"


def vte_new_tab_cwd() -> None:
    """This prints an escape sequence that tells VTE terminals the hostname
    and pwd. This should not be needed in most cases, but sometimes is for
    certain Linux terminals that do not read the PWD from the environment
    on startup. Note that this does not return a string, it simply prints
    and flushes the escape sequence to stdout directly.
    """
    env = XSH.env
    t = "\033]7;file://{}{}\007"
    s = t.format(env.get("HOSTNAME"), env.get("PWD"))
    print(s, end="", flush=True)

#
# job
#
"""Prompt formatter for current jobs"""

xj = _LazyModule.load('xonsh', 'xonsh.jobs', 'xj')
def _current_job():
    j = xj.get_next_task()
    if j is not None:
        if not j["bg"]:
            cmd = j["cmds"][-1]
            s = cmd[0]
            if s == "sudo" and len(cmd) > 1:
                s = cmd[1]
            return s

#
# times
#
"""date & time related prompt formatter"""
time = _LazyModule.load('time', 'time')
# amalgamated from xonsh.built_ins import XSH
def _localtime():
    pf = XSH.env.get("PROMPT_FIELDS", {})
    tf = pf.get("time_format", "%H:%M:%S")
    return time.strftime(tf, time.localtime())

#
# vc
#
"""Prompt formatter for simple version control branches"""
# pylint:disable=no-member, invalid-name
contextlib = _LazyModule.load('contextlib', 'contextlib')
# amalgamated os
pathlib = _LazyModule.load('pathlib', 'pathlib')
queue = _LazyModule.load('queue', 'queue')
# amalgamated re
subprocess = _LazyModule.load('subprocess', 'subprocess')
# amalgamated sys
threading = _LazyModule.load('threading', 'threading')
# amalgamated xonsh.tools
# amalgamated from xonsh.built_ins import XSH
from xonsh.lazyasd import LazyObject

RE_REMOVE_ANSI = LazyObject(
    lambda: re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]"),
    globals(),
    "RE_REMOVE_ANSI",
)


def _run_git_cmd(cmd):
    # create a safe detyped env dictionary and update with the additional git environment variables
    # when running git status commands we do not want to acquire locks running command like git status
    denv = dict(XSH.env.detype())
    denv.update({"GIT_OPTIONAL_LOCKS": "0"})
    return subprocess.check_output(cmd, env=denv, stderr=subprocess.DEVNULL)


def _get_git_branch(q):
    # from https://git-blame.blogspot.com/2013/06/checking-current-branch-programatically.html
    for cmds in [
        "git symbolic-ref --short HEAD",
        "git show-ref --head -s --abbrev",  # in detached mode return sha1
    ]:
        with contextlib.suppress(subprocess.CalledProcessError, OSError):
            branch = xt.decode_bytes(_run_git_cmd(cmds.split()))
            if branch:
                q.put(branch.splitlines()[0])
                return
    # all failed
    q.put(None)


def get_git_branch():
    """Attempts to find the current git branch. If this could not
    be determined (timeout, not in a git repo, etc.) then this returns None.
    """
    branch = None
    timeout = XSH.env.get("VC_BRANCH_TIMEOUT")
    q = queue.Queue()

    t = threading.Thread(target=_get_git_branch, args=(q,))
    t.start()
    t.join(timeout=timeout)
    try:
        branch = q.get_nowait()
        if branch:
            branch = RE_REMOVE_ANSI.sub("", branch)
    except queue.Empty:
        branch = None
    return branch


def _get_hg_root(q):
    _curpwd = XSH.env["PWD"]
    while True:
        if not os.path.isdir(_curpwd):
            return False
        try:
            dot_hg_is_in_curwd = any([b.name == ".hg" for b in os.scandir(_curpwd)])
        except OSError:
            return False
        if dot_hg_is_in_curwd:
            q.put(_curpwd)
            break
        else:
            _oldpwd = _curpwd
            _curpwd = os.path.split(_curpwd)[0]
            if _oldpwd == _curpwd:
                return False


def get_hg_branch(root=None):
    """Try to get the mercurial branch of the current directory,
    return None if not in a repo or subprocess.TimeoutExpired if timed out.
    """
    env = XSH.env
    timeout = env["VC_BRANCH_TIMEOUT"]
    q = queue.Queue()
    t = threading.Thread(target=_get_hg_root, args=(q,))
    t.start()
    t.join(timeout=timeout)
    try:
        root = pathlib.Path(q.get_nowait())
    except queue.Empty:
        return None
    if env.get("VC_HG_SHOW_BRANCH"):
        # get branch name
        branch_path = root / ".hg" / "branch"
        if branch_path.exists():
            with open(branch_path) as branch_file:
                branch = branch_file.read().strip()
        else:
            branch = "default"
    else:
        branch = ""
    # add activated bookmark and topic
    for filename in ["bookmarks.current", "topic"]:
        feature_branch_path = root / ".hg" / filename
        if feature_branch_path.exists():
            with open(feature_branch_path) as file:
                feature_branch = file.read().strip()
            if feature_branch:
                if branch:
                    if filename == "topic":
                        branch = f"{branch}/{feature_branch}"
                    else:
                        branch = f"{branch}, {feature_branch}"
                else:
                    branch = feature_branch

    return branch


_FIRST_BRANCH_TIMEOUT = True


def _first_branch_timeout_message():
    global _FIRST_BRANCH_TIMEOUT
    sbtm = XSH.env["SUPPRESS_BRANCH_TIMEOUT_MESSAGE"]
    if not _FIRST_BRANCH_TIMEOUT or sbtm:
        return
    _FIRST_BRANCH_TIMEOUT = False
    print(
        "xonsh: branch timeout: computing the branch name, color, or both "
        "timed out while formatting the prompt. You may avoid this by "
        "increasing the value of $VC_BRANCH_TIMEOUT or by removing branch "
        "fields, like {curr_branch}, from your $PROMPT. See the FAQ "
        "for more details. This message will be suppressed for the remainder "
        "of this session. To suppress this message permanently, set "
        "$SUPPRESS_BRANCH_TIMEOUT_MESSAGE = True in your xonshrc file.",
        file=sys.stderr,
    )


def _vc_has(binary):
    """This allows us to locate binaries after git only if necessary"""
    cmds = XSH.commands_cache
    if cmds.is_empty():
        return bool(cmds.locate_binary(binary, ignore_alias=True))
    else:
        return bool(cmds.lazy_locate_binary(binary, ignore_alias=True))


def current_branch():
    """Gets the branch for a current working directory. Returns an empty string
    if the cwd is not a repository.  This currently only works for git and hg
    and should be extended in the future.  If a timeout occurred, the string
    '<branch-timeout>' is returned.
    """
    branch = None
    if _vc_has("git"):
        branch = get_git_branch()
    if not branch and _vc_has("hg"):
        branch = get_hg_branch()
    if isinstance(branch, subprocess.TimeoutExpired):
        branch = "<branch-timeout>"
        _first_branch_timeout_message()
    return branch or None


def _git_dirty_working_directory(q, include_untracked):
    try:
        cmd = ["git", "status", "--porcelain"]
        if include_untracked:
            cmd += ["--untracked-files=normal"]
        else:
            cmd += ["--untracked-files=no"]
        status = _run_git_cmd(cmd)
        if status is not None:
            q.put(bool(status))
        else:
            q.put(None)
    except (subprocess.CalledProcessError, OSError):
        q.put(None)


def git_dirty_working_directory():
    """Returns whether or not the git directory is dirty. If this could not
    be determined (timeout, file not found, etc.) then this returns None.
    """
    env = XSH.env
    timeout = env.get("VC_BRANCH_TIMEOUT")
    include_untracked = env.get("VC_GIT_INCLUDE_UNTRACKED")
    q = queue.Queue()
    t = threading.Thread(
        target=_git_dirty_working_directory, args=(q, include_untracked)
    )
    t.start()
    t.join(timeout=timeout)
    try:
        return q.get_nowait()
    except queue.Empty:
        return None


def hg_dirty_working_directory():
    """Computes whether or not the mercurial working directory is dirty or not.
    If this cannot be determined, None is returned.
    """
    env = XSH.env
    cwd = env["PWD"]
    denv = env.detype()
    vcbt = env["VC_BRANCH_TIMEOUT"]
    # Override user configurations settings and aliases
    denv["HGRCPATH"] = ""
    try:
        s = subprocess.check_output(
            ["hg", "identify", "--id"],
            stderr=subprocess.PIPE,
            cwd=cwd,
            timeout=vcbt,
            universal_newlines=True,
            env=denv,
        )
        return s.strip(os.linesep).endswith("+")
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ):
        return None


def dirty_working_directory():
    """Returns a boolean as to whether there are uncommitted files in version
    control repository we are inside. If this cannot be determined, returns
    None. Currently supports git and hg.
    """
    dwd = None
    if _vc_has("git"):
        dwd = git_dirty_working_directory()
    if dwd is None and _vc_has("hg"):
        dwd = hg_dirty_working_directory()
    return dwd


def branch_color():
    """Return red if the current branch is dirty, yellow if the dirtiness can
    not be determined, and green if it clean. These are bold, intense colors
    for the foreground.
    """
    dwd = dirty_working_directory()
    if dwd is None:
        color = "{BOLD_INTENSE_YELLOW}"
    elif dwd:
        color = "{BOLD_INTENSE_RED}"
    else:
        color = "{BOLD_INTENSE_GREEN}"
    return color


def branch_bg_color():
    """Return red if the current branch is dirty, yellow if the dirtiness can
    not be determined, and green if it clean. These are background colors.
    """
    dwd = dirty_working_directory()
    if dwd is None:
        color = "{BACKGROUND_YELLOW}"
    elif dwd:
        color = "{BACKGROUND_RED}"
    else:
        color = "{BACKGROUND_GREEN}"
    return color

