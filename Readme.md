# Simple Test Case Maintainence

Since most test cases are repetition of smaller steps, this is a simple test-case expander script.

* Keep the simple steps defined in `StepBlock`s
* Define a `TestCase` as a collection of steps directly or as StepBlocks
* Run the script so that it expands the TestCases from StepBlocks
* One can then just copy paste the expanded result.

A sample test-case definition is provided.

```
$ ./TestCaseExpander.py -w SampleTestCase.tdef -o SampleTestCaseExpanded.tdef 
Created StepBlock:PingFromWClient
Created StepBlock:PingFromEClientGood
Created StepBlock:PingFromEClientBad
Created StepBlock:SetupTcpDumpEclient
Created TestCase:SimpleTestCase
$
```

Happy Testing!
