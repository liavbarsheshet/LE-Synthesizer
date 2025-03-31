const modes = [{
    headline: "User Input",
    desc: `Feel free to explore and experiment with our synthesizer by providing your own custom inputs.`,
    env: {
        p: [`True`], q: [`True`], linv: `False`, program: ``
    },
}, // Examples without Holes.
    {
        headline: "HW3 Testing",
        desc: `This example is sourced from the main file of Exercise 3.`,
        env: {
            p: [`True`], q: [`a == b`], linv: `a == b`, program: `a := b ; while i < n do ( a := a + 1 ; b := b + 1 )`
        },
    }, {
        headline: "HW3 Testing",
        desc: `This example demonstrates a simple loop that decrements two variables.`,
        env: {
            p: [`m >= 0`],
            q: [`(x == 0) and (y == m)`],
            linv: `( (x + y) == m ) and ( x >= 0 )`,
            program: `x := m ; y := 0 ; while x > 0 do ( x := x - 1 ; y := y + 1 )`
        },
    }, {
        headline: "HW3 Testing",
        desc: `This example involves multiplying two numbers using repeated addition.`,
        env: {
            p: [`b >= 0`],
            q: [`product == ( a * b )`],
            linv: `( product == ( a * count ) ) and ( count <= b )`,
            program: `product := 0 ; count := 0 ; while count < b do ( product := product + a ; count := count + 1 )`
        },
    }, {
        headline: "HW3 Testing",
        desc: `This example illustrates swapping the values of two variables.`,
        env: {
            p: [`True`],
            q: [`(x == y_init) and (y == x_init)`],
            linv: `False`,
            program: `x_init := x; y_init:=y ; temp := x ; x := y ; y := temp`
        },
    }, {
        headline: "HW3 Testing",
        desc: `This example finds the sum of numbers from 1 to n using a loop.`,
        env: {
            p: [`n >= 0`],
            q: [`sum == ( n * ( n + 1 ) )`],
            linv: `( sum == ( i * ( i + 1 ) ) ) and ( i <= n )`,
            program: `sum := 0 ; i := 0 ; while i < n do (  i := i + 1; sum := sum + ( 2 * i ) )`
        },
    },
    {
        headline: "Simple PBE",
        desc: `This example demonstrate simple pbe.`,
        env: {
            p: [`x == 2`],
            q: [`x == 8`],
            linv: `False`,
            program: `x := x * ??`
        },
    }, {
        headline: "Simple Assert",
        desc: `This example demonstrate simple assert.`,
        env: {
            p: [`x == 2`],
            q: [`True`],
            linv: `False`,
            program: `x := x * ??; assert x == 8`
        },
    },
    {
        headline: "Assert",
        desc: `This example demonstrate simple assert.`,
        env: {
            p: [`( product == 0 ) and ( b == 5 )`],
            q: [`( product == 25 ) and ( b == 5 )`],
            linv: `b >= 0`,
            program: `product := b * ?? ; assert ( product ) == ( b * 5 ) ; if product == 0 then while b < 5 do (b := b + 1) else b := 5`
        },
    },
    {
        headline: "Cube Calculation",
        desc: "This example calculates the cube of n minus an unknown value.",
        env: {
            p: ["( n == 3 ) and ( cube == 0 )"],
            q: ["( n == 3 ) and ( cube == 24 )"],
            linv: "False",
            program: "cube := ( ( ( n * n ) * n ) - ?? )"
        }
    },
    {
        headline: "Sum Calculation",
        desc: "This example sums two numbers a and b plus an unknown value.",
        env: {
            p: ["( ( a == 3 ) and ( b == 4 ) ) and ( sum == 0 )"],
            q: ["( ( a == 3 ) and ( b == 4 ) ) and ( sum == 10 )"],
            linv: "False",
            program: "sum := ( ( a + b ) + ?? )"
        }
    },
    {
        headline: "Product Calculation",
        desc: "This example calculates the product of c and d times an unknown value.",
        env: {
            p: ["( ( c == 2 ) and ( d == 6 ) ) and ( product == 0 )"],
            q: ["( ( c == 2 ) and ( d == 6 ) ) and ( product == 24 )"],
            linv: "False",
            program: "product := ( ( c * d ) * ?? )"
        }
    },
    {
        headline: "t Calculation",
        desc: "This example calculates the product of x times an unknown value assigned to t.",
        env: {
            p: ["( t == 0 ) and ( x == 2 )", "( t == 0 ) and ( x == 3 )"],
            q: ["( t == 6 ) and ( x == 2 )", "( t == 9 ) and ( x == 3 )"],
            linv: "False",
            program: "t := x * ??"
        }
    },
    {
        headline: "Difference Calculation",
        desc: "This example calculates the difference of e and f minus an unknown value.",
        env: {
            p: ["( ( e == 8 ) and ( f == 3 ) ) and ( difference == 0 )"],
            q: ["( ( e == 8 ) and ( f == 3 ) ) and ( difference == 2 )"],
            linv: "False",
            program: "difference := ( ( e - f ) - ?? )"
        }
    },
    {
        headline: "Modulo",
        desc: "This example calculates the power of k to the l and another power operation with an unknown value.",
        env: {
            p: ["x == 5"],
            q: ["( x == 5 ) and ( result == 1 )"],
            linv: "False",
            program: "result := x % ??"
        }
    },
    {
        headline: "Simple Calculation",
        desc: "This example demonstrates simple arithmetic.",
        env: {
            p: ["( x == 1 ) and ( y == 2 )"],
            q: ["( x == 2 ) and ( y == 4 )"],
            linv: "False",
            program: "x := x + 1 ; y := y * 2"
        }
    },
    {
        headline: "Simple Condition",
        desc: "This example demonstrates a simple conditional statement.",
        env: {
            p: ["( x == 3 ) and ( y == 4 )"],
            q: ["( x == 7 ) and ( y == 4 ) "],
            linv: "False",
            program: "x := x + y ; if ( ( x * y ) < 10 ) then y := y + 1 else skip"
        }
    },
    {
        headline: "Simple Loop Reduction",
        desc: "This example reduces y to zero in a loop.",
        env: {
            p: ["( y == 4 )"],
            q: ["( y == 0 )"],
            linv: "y >= 0",
            program: "while ( y > 0 ) do ( y := y - 1 )"
        }
    },
    {
        headline: "Conditional Loop",
        desc: "This example shows a loop with conditional statements.",
        env: {
            p: ["( y <= i ) and ( x == 3 )"],
            q: ["y >= i"],
            linv: "y <= i",
            program: "while ( y < i ) do ( x := x + y ; if ( ( x * y ) < 10 ) then y := y + 1 else skip )"
        }
    },
    {
        headline: "Increasing Sequence Validation",
        desc: "This example checks if the sequence values are increasing.",
        env: {
            p: ["( ( n == 3 ) and ( valid == True ) ) and ( prev == 2 )"],
            q: ["( ( n == 3 ) and ( valid == True ) ) and ( prev == 3 )"],
            linv: "False",
            program: "valid := ?? ; assert ( n > prev ) ; prev := n"
        }
    },
    {
        headline: "Simple Calculator",
        desc: "This example performs a basic calculation.",
        env: {
            p: ["( ( x == 1 ) and ( y == 2 ) ) and ( result == 0 )"],
            q: ["( ( x == 1 ) and ( y == 2 ) ) and ( result == 3 )"],
            linv: "False",
            program: "result := ?? ; assert ( result == ( x + y ) )"
        }
    },
    {
        headline: "Product Calculation with Assert",
        desc: "This example calculates the product of b with an unknown value and asserts it.",
        env: {
            p: ["( product == 0 ) and ( b == 5 )"],
            q: ["( product == 25 ) and ( b == 5 )"],
            linv: "b >= 0",
            program: "product := ( b * ?? ) ; assert ( product == ( b * 5 ) ) ; if product == 0 then while b < 5 do ( b := b + 1 ) else b := 5"
        }
    },
    {
        headline: "Product Calculation with Assert - Different Multiplier",
        desc: "This example calculates the product of b with an unknown value and asserts it using a different multiplier.",
        env: {
            p: ["( product == 0 ) and ( b == 4 )"],
            q: ["( product == 16 ) and ( b == 4 )"],
            linv: "( b >= 0 )",
            program: "product := ( b * ?? ) ; assert ( product == ( b * 4 ) ) ; skip"
        }
    },
    {
        headline: "Product Calculation",
        desc: "This example calculates the product of b multiplied by an unknown value.",
        env: {
            p: ["( product == 0 ) and ( b == 4 )"],
            q: ["( product == 16 ) and ( b == 0 )"],
            linv: "False",
            program: "product := ( b * ?? ) ; assert ( product == ( b * 4 ) ) ; if ( product == 0 ) then ( b := 4 ) else ( b := 0 )"
        }
    },
    {
        headline: "Product Calculation with Assertion",
        desc: "This example calculates the product of b times an unknown value and checks assertions.",
        env: {
            p: ["( product == 0 ) and ( b == 8 )"],
            q: ["( product == 32 ) and ( b == 0 )"],
            linv: "b >= 0",
            program: "product := ( b * ?? ) ; assert ( product == ( b * 4 ) ) ; if ( product == 0 ) then b := 8 else b := 0"
        }
    },
    {
        headline: "Multiplication Product Example",
        desc: "This example calculates the product of b times an unknown value and includes a conditional statement.",
        env: {
            p: ["( product == 0 ) and ( b == 6 )"],
            q: ["( product == 18 ) and ( b == 3 )"],
            linv: "b >= 0",
            program: "product := ( b * ?? ) ; assert ( product == ( b * 3 ) ) ; if ( product == 0 ) then b := 6 else b := 3"
        }
    },
    {
        headline: "Sum Calculation with Condition",
        desc: "This example calculates the sum of a and an unknown value, asserts the result, and includes a conditional statement.",
        env: {
            p: ["( sum == 0 ) and ( a == 8 )"],
            q: ["( sum == 13 ) and ( a == 3 )"],
            linv: "a >= 0",
            program: "sum := ( a + ?? ) ; assert ( sum == ( a + 5 ) ) ; if ( sum == 0 ) then a := 8 else a := 3"
        }
    },
    {
        headline: "Multiplication and Loop Example",
        desc: "This example multiplies b by an unknown value, asserts the result, and includes a while loop that decrements b.",
        env: {
            p: ["( a == 0 ) and ( b == 6 )"],
            q: ["( a == 0 ) and ( b == 0 )"],
            linv: "b >= 0",
            program: "a := ( b * ?? ) ; assert ( a == ( b * 6 ) ) ; while ( b > 0 ) do ( b := b - 1 )"
        }
    },
    {
        headline: "Product Calculation and Conditional Loop",
        desc: "This example calculates the product of b and an unknown value, asserts the result, and includes a conditional loop that increments b or sets it to 2.",
        env: {
            p: ["( product == 0 ) and ( b == 3 )"],
            q: ["( product == 6 ) and ( b == 2 )"],
            linv: "b >= 0",
            program: "product := ( b * ?? ) ; assert ( product == ( b * 2 ) ) ; if ( product == 0 ) then while ( b < 3 ) do ( b := b + 1 ) else b := 2"
        }
    },
    {
        headline: "Product Addition and Conditional Loop",
        desc: "This example calculates the sum of b and an unknown value, asserts the result as a product, and includes a conditional loop that increments b or sets it to 2.",
        env: {
            p: ["( product == 0 ) and ( b == 3 )"],
            q: ["( product == 6 ) and ( b == 2 )"],
            linv: "b >= 0",
            program: "product := ( b + ?? ) ; assert ( product == ( b * 2 ) ) ; if ( product == 0 ) then while ( b < 3 ) do ( b := b + 1 ) else b := 2"
        }
    },
    {
        headline: "Product Calculation with Nested Conditions",
        desc: "This example calculates the product of b times an unknown value, asserts the result, and includes nested conditions to modify the value of b.",
        env: {
            p: ["( product == 0 ) and ( b == 8 )"],
            q: ["( product == 32 ) and ( b == 0 )"],
            linv: "b >= 0",
            program: "product := ( b * ?? ) ; assert ( product == ( b * 4 ) ) ; if ( product == 0 ) then b := 8 else if ( b < 4 ) then b := 4 else b := 0"
        }
    },
    {
        headline: "Multiple Inputs (Without holes)",
        desc: "This example verifies a program with multiple inputs.",
        env: {
            p: ["p == 16", "q == 17", "r == 18", "s == 19", "t == 20", "u == 21", "v == 22"],
            q: ["p == 17", "q == 18", "r == 19", "s == 20", "t == 21", "u == 22", "v == 23"],
            linv: "False",
            program: "p := p + 1 ; q := q + 1 ; r := r + 1 ; s := s + 1 ; t := t + 1 ; u := u + 1 ; v := v + 1"
        }
    },
    {
        headline: "Multiple Inputs (With holes)",
        desc: "This example verifies and sketches a program with multiple inputs.",
        env: {
            p: ["a == 1", "b == 2", "c == 3"],
            q: ["a == 1", "b == 40", "c == 81"],
            linv: "False",
            program: "a := a * ?? ; b := b * ??; c := c * ??"
        }
    },
    {
        headline: "Bizarre Sketch",
        desc: "This example verifies and sketches a program.",
        env: {
            p: ["g == 2"],
            q: ["g == 100"],
            linv: "False",
            program: "g := g + ?? ; g := g * ?? ; g := g - ?? ; g := g / ?? ; g := g * ?? ; g := g + ??"
        }
    },
    {
        headline: "Multiple Expressions (Without Holes)",
        desc: "This example verifies a program with multiple expressions.",
        env: {
            p: ["( x == 0 ) and ( y == 0 )"],
            q: ["( x == 10 ) and ( y == -5 )"],
            linv: "False",
            program: "x := x + 1 ; x := x + 2 ; x := x + 3 ; x := x + 4 ; y := y - 1 ; y := y - 2 ; y := y - 2"
        }
    },
    {
        headline: "Loop Unrolling",
        desc: "This example verifies and sketches a program with unrolling technique.",
        env: {
            p: ["(x == 0) and (i == 0)"],
            q: ["(x == 12) and (i == 0)"],
            linv: "(i >= 0) and ( x == ( 2 * (6 - i)))",
            program: "i := ?? ;assert i==6; while i > 0 do (x := x + ??; i := i - 1)"
        }
    },
]

const selection = document.getElementById("mode");
const modeHeadline = document.getElementById("mode-headline");
const modeDesc = document.getElementById("mode-description");
const form = document.getElementById("synthesis");
const output = document.getElementById("console");
const add_more = document.getElementById("add_more")
const more_inputs = document.getElementById("more_inputs")


/* Mode Selection */
modes.forEach((({headline}, index) => {
    if (!index)
        selection.innerHTML += `<option value="${index}" selected>${headline}</option>`
    else
        selection.innerHTML += `<option value="${index}" >Example ${index} - ${headline}</option>`
}))

const onChange = () => {
    const value = parseInt(selection.value);

    if (!(value in modes)) return;

    const current = modes[value];

    if (modeHeadline) modeHeadline.innerHTML = !value ? current.headline : `Example ${value} - ${current.headline}`;
    if (modeDesc) modeDesc.innerHTML = current.desc;

    const inputs = form?.querySelectorAll("input[name],textarea[name]") ?? [];

    const env = current?.env ?? {};

    inputs.forEach(input => {
        const {name} = input;

        if (!env[name]) {
            input.value = "";
            return;
        }
        input.value = env[name];
    });

    // Parsing P and Q
    if (!env.q?.length || !env.p?.length || env.q?.length !== env.p?.length) return insert_input();

    handle_clear_inputs()

    for (let i = 0; i < env.q.length; ++i) {
        const value = {q: env.q[i], p: env.p[i]}
        insert_input(value);
    }


}

// Trigger manually
/* Mode Selection - END */


/* Form Section */
let busy = false;
let request_num = 0;

const parseResponse = (response) => {
    console.log(response)
    if (!response.output || response.output?.length === 0) response.output = `
         <li>
                Outputs: <span data-completed="${response.completed === true}">Nothing to show...</span>
        </li>
        `
    else response.output = `
            <li>
                Outputs:
                <br />
                <ul>
                     ${(response.output ?? []).map(output => `<li>${output}</li>`).join('')}
                </ul> 
            </li>
        `
    return `
        ${request_num > 1 ? `<hr class="dashed"/>` : ''}
        <h6>[ <span class="console-status extra-bold">${request_num}</span> ] Response: <span data-completed="${response.completed === true}">${response.message ?? ""}</span></h6>
        <ul>
            ${response.output}
            <li>Mode: <span class="console-status">${selection.options[selection.value]?.innerText}</span></li>
            <li>Status Code: <span class="console-status">${response.status_code}</span></li>
            <li>Completed: <span class="console-status">${response.completed}</span></li>
            <li>Arrival: <span class="console-status">${response.arrival}</span></li>
            <li>Elapsed: <span class="console-status">${response.elapsed}s</span></li>
        </ul>  
`
}

const toggleInputs = (isDisabled = false) => {
    const inputs = form?.querySelectorAll("input[name],textarea[name]") ?? [];
    inputs.forEach(input => {
        input.disabled = isDisabled;
    })
    form?.setAttribute("data-loading", `${isDisabled}`);
}

// Performs the submit action
const onSubmit = (event) => {
    event.preventDefault();

    if (busy || !form) return;

    if (!form.checkValidity()) return;

    busy = true;

    const data = {};

    // Converting data to json object
    (new FormData(form)).forEach((value, key) => {
        data[key] = value;
    });

    toggleInputs(true);

    request_num += 1;

    // Making the request
    fetch('/synthesize', {
        method: 'POST', // Specify the request method
        headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(result => {
            const parsed_response = parseResponse(result);
            output.innerHTML += parsed_response;
        })
        .catch(error => {
            const parsed_response = parseResponse({
                message: error.message, arrival: -1, elapsed: -1, outputs: [], completed: false, status_code: 500
            });
            output.innerHTML += parsed_response;
        })
        .finally(() => {
            toggleInputs();
            if (output) {
                output.scrollIntoView({behavior: 'smooth', block: 'start'});
                output.scrollTop = output.scrollHeight;
            }
            busy = false;
        });
}

const onReset = (e) => {
    e.preventDefault();
    onChange();
}

form?.addEventListener("submit", onSubmit);
form?.addEventListener("reset", onReset);
/* Form Section - END */


/* Add More Inputs Outputs */
let total_ios = 0;

const aux_create_new_input = (name, index, value) => {
    const input = document.createElement("input");
    input.type = "text"
    input.value = value ?? "True"
    input.name = `${name}${index}`
    input.id = `${name}${index}`
    const label = document.createElement("label")
    label.for = `${name}${index}`
    label.innerHTML = `${name.toUpperCase()}`

    return [label, input]
}
const insert_input = (value = {}) => {
    const {p, q} = value;
    const new_index = total_ios;

    ++total_ios;

    const io = []

    const small = document.createElement("small");

    small.innerHTML = new_index === 0 ? "Inputs / Outputs" : `Additional Input / Output`;

    const div = document.createElement("div")
    div.className = "input-ui"
    div.append(small)

    io.push(div)
    io.push(...aux_create_new_input("p", new_index, p));
    io.push(...aux_create_new_input("q", new_index, q));

    io.forEach(node => more_inputs.append(node))

    if (new_index > 0) {
        const remove_bt = document.createElement("button");
        remove_bt.className = "remove-bt";
        remove_bt.innerHTML = "X"
        remove_bt.onclick = () => handle_remove(io)
        div.append(remove_bt)
    }
}

const handle_remove = (io) => {
    io.forEach(node => node.remove())
}

const handle_clear_inputs = () => {
    while (more_inputs.firstChild) {
        more_inputs.removeChild(more_inputs.firstChild);
    }
    total_ios = 0;
}

add_more?.addEventListener("click", insert_input);
selection?.addEventListener("change", onChange);
onChange();

/* Cleaning */

window.addEventListener('beforeunload', function () {
    selection?.removeEventListener("change", onChange);
    form?.removeEventListener('submit', onSubmit);
    add_more?.removeEventListener("click", insert_input);
});