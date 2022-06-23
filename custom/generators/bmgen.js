class CustomGenerator {
  /**
   * @param {string} name Language name of this generator.
   */
  constructor(name) {
    this.name_ = name;

    /**
     * This is used as a placeholder in functions defined using
     * Generator.provideFunction_.  It must not be legal code that could
     * legitimately appear in a function definition (or comment), and it must
     * not confuse the regular expression parser.
     * @type {string}
     * @protected
     */
    this.FUNCTION_NAME_PLACEHOLDER_ = '{leCUI8hutHZI4480Dc}';

    this.FUNCTION_NAME_PLACEHOLDER_REGEXP_ =
      new RegExp(this.FUNCTION_NAME_PLACEHOLDER_, 'g');

    /**
     * Arbitrary code to inject into locations that risk causing infinite loops.
     * Any instances of '%1' will be replaced by the block ID that failed.
     * E.g. '  checkTimeout(%1);\n'
     * @type {?string}
     */
    this.INFINITE_LOOP_TRAP = null;

    /**
     * Arbitrary code to inject before every statement.
     * Any instances of '%1' will be replaced by the block ID of the statement.
     * E.g. 'highlight(%1);\n'
     * @type {?string}
     */
    this.STATEMENT_PREFIX = null;

    /**
     * Arbitrary code to inject after every statement.
     * Any instances of '%1' will be replaced by the block ID of the statement.
     * E.g. 'highlight(%1);\n'
     * @type {?string}
     */
    this.STATEMENT_SUFFIX = null;

    /**
     * The method of indenting.  Defaults to two spaces, but language generators
     * may override this to increase indent or change to tabs.
     * @type {string}
     */
    this.INDENT = '  ';

    /**
     * Maximum length for a comment before wrapping.  Does not account for
     * indenting level.
     * @type {number}
     */
    this.COMMENT_WRAP = 60;

    /**
     * List of outer-inner pairings that do NOT require parentheses.
     * @type {!Array<!Array<number>>}
     */
    this.ORDER_OVERRIDES = [];

    /**
     * Whether the init method has been called.
     * Generators that set this flag to false after creation and true in init
     * will cause blockToCode to emit a warning if the generator has not been
     * initialized. If this flag is untouched, it will have no effect.
     * @type {?boolean}
     */
    this.isInitialized = null;

    /**
     * Comma-separated list of reserved words.
     * @type {string}
     * @protected
     */
    this.RESERVED_WORDS_ = '';

    /**
     * A dictionary of definitions to be printed before the code.
     * @type {!Object|undefined}
     * @protected
     */
    this.definitions_ = undefined;

    /**
     * A dictionary mapping desired function names in definitions_ to actual
     * function names (to avoid collisions with user functions).
     * @type {!Object|undefined}
     * @protected
     */
    this.functionNames_ = undefined;

    /**
     * A database of variable and procedure names.
     * @type {!Names|undefined}
     * @protected
     */
    this.nameDB_ = undefined;

    this.channels = [];
    this.variables = [];
  }

  /**
   * Generate code for all blocks in the workspace to the specified language.
   * @param {!Workspace=} workspace Workspace to generate code from.
   * @return {string} Generated code.
   */
  workspaceToCode(workspace) {
    if (!workspace) {
      // Backwards compatibility from before there could be multiple workspaces.
      console.warn(
        'No workspace specified in workspaceToCode call.  Guessing.');
      workspace = common.getMainWorkspace();
    }
    let code = [];
    this.init(workspace);
    const blocks = workspace.getTopBlocks(true);
    for (let i = 0, block; (block = blocks[i]); i++) {
      const blockcode = this.blockToCode(block)
      if (blockcode)
        code.push(blockcode);
    }
    code = code.join('\n');
    code = this.finish(code);
    return code;
  }

  // The following are some helpful functions which can be used by multiple

  // languages.

  /**
   * Prepend a common prefix onto each line of code.
   * Intended for indenting code or adding comment markers.
   * @param {string} text The lines of code.
   * @param {string} prefix The common prefix.
   * @return {string} The prefixed lines of code.
   */
  prefixLines(text, prefix) {
    return prefix + text.replace(/(?!\n$)\n/g, '\n' + prefix);
  }

  /**
   * Recursively spider a tree of blocks, returning all their comments.
   * @param {!Block} block The block from which to start spidering.
   * @return {string} Concatenated list of comments.
   */
  allNestedComments(block) {
    const comments = [];
    const blocks = block.getDescendants(true);
    for (let i = 0; i < blocks.length; i++) {
      const comment = blocks[i].getCommentText();
      if (comment) {
        comments.push(comment);
      }
    }
    // Append an empty string to create a trailing line break when joined.
    if (comments.length) {
      comments.push('');
    }
    return comments.join('\n');
  }

  /**
   * Generate code for the specified block (and attached blocks).
   * The generator must be initialized before calling this function.
   * @param {?Block} block The block to generate code for.
   * @param {boolean=} opt_thisOnly True to generate code for only this
   *     statement.
   * @return {string|!Array} For statement blocks, the generated code.
   *     For value blocks, an array containing the generated code and an
   *     operator order value.  Returns '' if block is null.
   */
  blockToCode(block, opt_thisOnly) {
    if (this.isInitialized === false) {
      console.warn(
        'Generator init was not called before blockToCode was called.');
    }
    if (!block) {
      return null;
    }
    if (!block.isEnabled()) {
      // Skip past this block if it is disabled.
      return opt_thisOnly ? '' : this.blockToCode(block.getNextBlock());
    }
    if (block.isInsertionMarker()) {
      // Skip past insertion markers.
      return opt_thisOnly ? '' : this.blockToCode(block.getChildren(false)[0]);
    }

    const func = this[block.type];
    if (typeof func !== 'function') {
      throw Error(
        'Language "' + this.name_ + '" does not know how to generate ' +
        'code for block type "' + block.type + '".');
    }
    // First argument to func.call is the value of 'this' in the generator.
    // Prior to 24 September 2013 'this' was the only way to access the block.
    // The current preferred method of accessing the block is through the second
    // argument to func.call, which becomes the first parameter to the
    // generator.
    let code = func.call(block, block);
    return this.scrub_(block, code, opt_thisOnly);
  }

  /**
   * Generate code representing the specified value input.
   * @param {!Block} block The block containing the input.
   * @param {string} name The name of the input.
   * @param {number} outerOrder The maximum binding strength (minimum order
   *     value) of any operators adjacent to "block".
   * @return {string} Generated code or '' if no blocks are connected or the
   *     specified input does not exist.
   */
  valueToCode(block, name) {
    const targetBlock = block.getInputTargetBlock(name);
    if (!targetBlock) {
      return '';
    }
    const code = this.blockToCode(targetBlock);
    return code;
  }

  /**
   * Generate a code string representing the blocks attached to the named
   * statement input. Indent the code.
   * This is mainly used in generators. When trying to generate code to evaluate
   * look at using workspaceToCode or blockToCode.
   * @param {!Block} block The block containing the input.
   * @param {string} name The name of the input.
   * @return {string} Generated code or '' if no blocks are connected.
   */
  statementToCode(block, name) {
    const targetBlock = block.getInputTargetBlock(name);
    let code = this.blockToCode(targetBlock);
    return code;
  }

  /**
   * Add an infinite loop trap to the contents of a loop.
   * Add statement suffix at the start of the loop block (right after the loop
   * statement executes), and a statement prefix to the end of the loop block
   * (right before the loop statement executes).
   * @param {string} branch Code for loop contents.
   * @param {!Block} block Enclosing block.
   * @return {string} Loop contents, with infinite loop trap added.
   */
  addLoopTrap(branch, block) {
    if (this.INFINITE_LOOP_TRAP) {
      branch = this.prefixLines(
        this.injectId(this.INFINITE_LOOP_TRAP, block), this.INDENT) +
        branch;
    }
    if (this.STATEMENT_SUFFIX && !block.suppressPrefixSuffix) {
      branch = this.prefixLines(
        this.injectId(this.STATEMENT_SUFFIX, block), this.INDENT) +
        branch;
    }
    if (this.STATEMENT_PREFIX && !block.suppressPrefixSuffix) {
      branch = branch +
        this.prefixLines(
          this.injectId(this.STATEMENT_PREFIX, block), this.INDENT);
    }
    return branch;
  }

  /**
   * Inject a block ID into a message to replace '%1'.
   * Used for STATEMENT_PREFIX, STATEMENT_SUFFIX, and INFINITE_LOOP_TRAP.
   * @param {string} msg Code snippet with '%1'.
   * @param {!Block} block Block which has an ID.
   * @return {string} Code snippet with ID.
   */
  injectId(msg, block) {
    const id = block.id.replace(/\$/g, '$$$$');  // Issue 251.
    return msg.replace(/%1/g, '\'' + id + '\'');
  }

  /**
   * Add one or more words to the list of reserved words for this language.
   * @param {string} words Comma-separated list of words to add to the list.
   *     No spaces.  Duplicates are ok.
   */
  addReservedWords(words) {
    this.RESERVED_WORDS_ += words + ',';
  }

  /**
   * Define a developer-defined function (not a user-defined procedure) to be
   * included in the generated code.  Used for creating private helper
   * functions. The first time this is called with a given desiredName, the code
   * is saved and an actual name is generated.  Subsequent calls with the same
   * desiredName have no effect but have the same return value.
   *
   * It is up to the caller to make sure the same desiredName is not
   * used for different helper functions (e.g. use "colourRandom" and
   * "listRandom", not "random").  There is no danger of colliding with reserved
   * words, or user-defined variable or procedure names.
   *
   * The code gets output when Generator.finish() is called.
   *
   * @param {string} desiredName The desired name of the function
   *     (e.g. mathIsPrime).
   * @param {!Array<string>|string} code A list of statements or one multi-line
   *     code string.  Use '  ' for indents (they will be replaced).
   * @return {string} The actual name of the new function.  This may differ
   *     from desiredName if the former has already been taken by the user.
   * @protected
   */
  provideFunction_(desiredName, code) {
    if (!this.definitions_[desiredName]) {
      const functionName =
        this.nameDB_.getDistinctName(desiredName, NameType.PROCEDURE);
      this.functionNames_[desiredName] = functionName;
      if (Array.isArray(code)) {
        code = code.join('\n');
      }
      let codeText = code.trim().replace(
        this.FUNCTION_NAME_PLACEHOLDER_REGEXP_, functionName);
      // Change all '  ' indents into the desired indent.
      // To avoid an infinite loop of replacements, change all indents to '\0'
      // character first, then replace them all with the indent.
      // We are assuming that no provided functions contain a literal null char.
      let oldCodeText;
      while (oldCodeText !== codeText) {
        oldCodeText = codeText;
        codeText = codeText.replace(/^(( {2})*) {2}/gm, '$1\0');
      }
      codeText = codeText.replace(/\0/g, this.INDENT);
      this.definitions_[desiredName] = codeText;
    }
    return this.functionNames_[desiredName];
  }

  /**
   * Hook for code to run before code generation starts.
   * Subclasses may override this, e.g. to initialise the database of variable
   * names.
   * @param {!Workspace} _workspace Workspace to generate code from.
   */
  init(_workspace) {
    // Optionally override
    // Create a dictionary of definitions to be printed before the code.
    this.definitions_ = Object.create(null);
    // Create a dictionary mapping desired developer-defined function names in
    // definitions_ to actual function names (to avoid collisions with
    // user-defined procedures).
    this.functionNames_ = Object.create(null);
  }

  /**
   * Common tasks for generating code from blocks.  This is called from
   * blockToCode and is called on every block, not just top level blocks.
   * Subclasses may override this, e.g. to generate code for statements
   * following the block, or to handle comments for the specified block and any
   * connected value blocks.
   * @param {!Block} _block The current block.
   * @param {string} code The code created for this block.
   * @param {boolean=} _opt_thisOnly True to generate code for only this
   *     statement.
   * @return {string} Code with comments and subsequent blocks added.
   * @protected
   */
  scrub_(_block, code, _opt_thisOnly) {
    // Optionally override
    return code;
  }

  /**
   * Hook for code to run at end of code generation.
   * Subclasses may override this, e.g. to prepend the generated code with
   * import statements or variable definitions.
   * @param {string} code Generated code.
   * @return {string} Completed code.
   */
  finish(code) {
    // Optionally override
    // Clean up temporary data.
    delete this.definitions_;
    delete this.functionNames_;
    return code;
  }

  /**
   * Naked values are top-level blocks with outputs that aren't plugged into
   * anything.
   * Subclasses may override this, e.g. if their language does not allow
   * naked values.
   * @param {string} line Line of generated code.
   * @return {string} Legal line of code.
   */
  scrubNakedValue(line) {
    // Optionally override
    return line;
  }
}

Object.defineProperties(CustomGenerator.prototype, {
  /**
   * A database of variable names.
   * @name Blockly.Generator.prototype.variableDB_
   * @type {!Names|undefined}
   * @protected
   * @deprecated 'variableDB_' was renamed to 'nameDB_' (May 2021).
   * @suppress {checkTypes}
   */
  variableDB_: {
    /**
     * @this {Generator}
     * @return {!Names|undefined} Name database.
     */
    get: function () {
      deprecation.warn('variableDB_', 'May 2021', 'May 2026', 'nameDB_');
      return this.nameDB_;
    },
    /**
     * @this {Generator}
     * @param {!Names|undefined} nameDb New name database.
     */
    set: function (nameDb) {
      deprecation.warn('variableDB_', 'May 2021', 'May 2026', 'nameDB_');
      this.nameDB_ = nameDb;
    },
  },
});

Blockly.BMGen = new CustomGenerator('BMGen');


Blockly.BMGen.scrub_ = function (block, code, opt_thisOnly) {
  const nextBlock = block.nextConnection && block.nextConnection.targetBlock();
  const nextCode = opt_thisOnly ? null : this.blockToCode(nextBlock);
  if (nextCode) {
    return code + '\n' + nextCode;
  } else {
    return code;
  }
};

Blockly.BMGen.fillDynamicCategoriesFromProgram = function (program) {
  const findObjects = function (root, type) {
    let list = [];
    if ('type' in root && root.type === type) {
      list.push(root);
    }
    for (const value of Object.values(root)) {
      if (typeof value === 'object' && value !== null) {
        list = list.concat(findObjects(value, type));
      }
    }
    return list;
  };

  let programVariables = findObjects(program, 'variable').map(x => x.name);
  this.variables = this.variables.concat(programVariables).filter((v, i, a) => a.indexOf(v) === i).sort();

  let programChannels = findObjects(program, 'channel').map(x => x.name);
  this.channels = this.channels.concat(programChannels).filter((v, i, a) => a.indexOf(v) === i).sort();
};

loadScript("custom/generators/bmgen/statements.js");
loadScript("custom/generators/bmgen/limits.js");
loadScript("custom/generators/bmgen/channels.js");
loadScript("custom/generators/bmgen/variables.js");
loadScript("custom/generators/bmgen/other.js");