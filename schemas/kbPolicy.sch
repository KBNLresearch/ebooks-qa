<?xml version="1.0"?>
<!--
   Schematron epubcheck schema: verify if EPUB conforms to
   minimal  profile (well-formed, no encrypted resources).
   Based on output of epubcheck using -out switch, which results in XML output that follows
   the JHOVE schema.
-->
<s:schema xmlns:s="http://purl.oclc.org/dsdl/schematron">
<s:ns uri="http://hul.harvard.edu/ois/xml/ns/jhove" prefix="jh"/>

  <!-- Validation status -->
  <s:pattern name="wellFormed">
    <s:rule context="/jh:jhove/jh:repInfo">
      <s:assert test="(jh:status = 'Well-formed')">Not well-formed epub</s:assert>
    </s:rule>
  </s:pattern>

  <!-- Encryption -->

  <!-- This rule rules out encrypted content, but permits font obfuscation-->  
  <s:pattern name="encryptedResources">
    <s:rule context="/jh:jhove/jh:repInfo/jh:messages">
      <s:assert test="count(jh:message[contains(.,'could not be decrypted')]) = 0">Contains encrypted resources</s:assert>
    </s:rule>
  </s:pattern>

  <!-- This rule rules out any sort of encryption, including font obfuscation-->  
  <!--s:pattern name="encryption">
    <s:rule context="/jh:jhove/jh:repInfo/jh:properties/jh:property">
      <s:assert test="(jh:name = 'hasEncryption' and jh:values/jh:value ='false') or (jh:name != 'hasEncryption')">Has encryption</s:assert>
    </s:rule>
  </s:pattern -->
  
</s:schema>
