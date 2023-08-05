'''
# cdktf-tf-module-stack

A drop-in replacement for cdktf.TerraformStack that let's you define Terraform modules as construct.

## Setup

### Node.js

Run `yarn add cdktf-tf-module-stack` (or `npm install --save cdktf-tf-module-stack`) to install the package.

### Python

Run `pip install cdktf-tf-module-stack` to install the package.

## Usage

```python
import { App } from "cdktf";
import { TFModuleStack, TFModuleVariable } from "cdktf-tf-module-stack";
import { NullProvider, Resource } from "@cdktf/provider-null";

class MyAwesomeModule extends TFModuleStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new NullProvider(this, "null");
    new Resource(this, "resource");

    new TFModuleVariable(this, "my_var", {
      type: "string",
      description: "A variable",
      default: "default",
    });
  }
}

const app = new App();
new MyAwesomeModule(app, "my-awesome-module");
app.synth();
```

This will synthesize a Terraform JSON file that looks like this:

```json
{
  "resource": {
    "null_resource": {
      "resource": {}
    }
  },
  "terraform": {
    "required_providers": {
      "null": {
        "source": "null",
        "version": "~> 2.0"
      }
    },
    "variable": {
      "my_var": {
        "default": "default",
        "description": "A variable",
        "type": "string"
      }
    }
  }
}
```

Please note that the provider section is missing, so that the Terraform Workspace using the generated module can be used with any provider matching the version.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import constructs


class TFModuleStack(
    cdktf.TerraformStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-tf-module-stack.TFModuleStack",
):
    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))


class TFModuleVariable(
    cdktf.TerraformVariable,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-tf-module-stack.TFModuleVariable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        default: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[builtins.bool] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param default: 
        :param description: 
        :param nullable: 
        :param sensitive: 
        :param type: (experimental) The type argument in a variable block allows you to restrict the type of value that will be accepted as the value for a variable. If no type constraint is set then a value of any type is accepted. While type constraints are optional, we recommend specifying them; they serve as easy reminders for users of the module, and allow Terraform to return a helpful error message if the wrong type is used. Type constraints are created from a mixture of type keywords and type constructors. The supported type keywords are: - string - number - bool The type constructors allow you to specify complex types such as collections: - list(<TYPE>) - set(<TYPE>) - map(<TYPE>) - object({<ATTR NAME> = <TYPE>, ... }) - tuple([<TYPE>, ...]) The keyword any may be used to indicate that any type is acceptable. For more information on the meaning and behavior of these different types, as well as detailed information about automatic conversion of complex types, see {@link https://www.terraform.io/docs/configuration/types.html|Type Constraints}. If both the type and default arguments are specified, the given default value must be convertible to the specified type.
        '''
        config = cdktf.TerraformVariableConfig(
            default=default,
            description=description,
            nullable=nullable,
            sensitive=sensitive,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, name, config])


__all__ = [
    "TFModuleStack",
    "TFModuleVariable",
]

publication.publish()
