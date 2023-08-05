## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="form_content()">

  <h3 class="block is-size-3">Display</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field message="If not set, vendor chooser is an autocomplete field.">
      <b-checkbox name="rattail.vendors.choice_uses_dropdown"
                  v-model="simpleSettings['rattail.vendors.choice_uses_dropdown']"
                  native-value="true"
                  @input="settingsNeedSaved = true">
        Show vendor chooser as dropdown (select) element
      </b-checkbox>
    </b-field>

  </div>
</%def>


${parent.body()}
